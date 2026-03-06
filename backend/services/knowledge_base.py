"""
Knowledge Base Service — fast in-memory BM25 search over scraped NEU pages.

At startup it loads `scraper/neu_scraped_data.json` (if it exists) and builds
an inverted index.  Every call to `search()` is pure Python — no API call, no
network round-trip — so it is nearly instantaneous.

Typical use inside bot_logic.py:

    from services.knowledge_base import kb

    result = kb.search(user_query, top_k=1)
    if result:
        answer, url = result[0]
        return f"{answer}<br><a href='{url}'>Source</a>"
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import defaultdict
from typing import Optional

# ─── Path resolution ─────────────────────────────────────────────────────────

_HERE = os.path.dirname(__file__)
_DATA_FILE = os.path.join(_HERE, "..", "scraper", "neu_scraped_data.json")
_DATA_FILE = os.path.normpath(_DATA_FILE)

# ─── Stop-words (kept small; enough to ignore noise without hurting recall) ──

STOP_WORDS = frozenset({
    "a", "an", "the", "is", "it", "in", "on", "at", "to", "of", "and",
    "or", "for", "with", "that", "this", "are", "was", "were", "be",
    "been", "have", "has", "had", "do", "does", "did", "will", "would",
    "can", "could", "may", "might", "shall", "should", "not", "no",
    "i", "we", "you", "he", "she", "they", "my", "our", "your", "its",
    "by", "from", "as", "if", "so", "but", "about", "which", "what",
    "how", "when", "where", "who", "there", "their", "them", "into",
    "than", "then", "also", "more", "any", "all", "neu", "university",
    "near", "east",
})

# BM25 hyper-parameters
BM25_K1 = 1.5
BM25_B  = 0.75

# Minimum score to be returned as a match
MIN_SCORE = 3.0

# Minimum answer content length
MIN_CONTENT_LEN = 80


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


class KnowledgeBase:
    """BM25 index over scraped NEU page chunks."""

    def __init__(self):
        self._chunks: list[dict] = []          # [{url, title, section, content}]
        self._index: dict[str, list[tuple[int, int]]] = defaultdict(list)
        # index[term] = [(doc_id, term_freq), ...]
        self._doc_lens: list[int] = []
        self._avg_dl: float = 0.0
        self._loaded = False

    # ─── Loading ─────────────────────────────────────────────────────────────

    def load(self, path: str = _DATA_FILE) -> int:
        """Load scraped data and build index. Returns number of chunks loaded."""
        if not os.path.exists(path):
            print(f"[KnowledgeBase] Data file not found: {path}. Run the crawler first.")
            return 0

        with open(path, "r", encoding="utf-8") as f:
            raw: list[dict] = json.load(f)

        # Filter short / empty chunks
        self._chunks = [c for c in raw if len(c.get("content", "")) >= MIN_CONTENT_LEN]

        # Build inverted index
        self._index.clear()
        self._doc_lens = []
        total_len = 0

        for doc_id, chunk in enumerate(self._chunks):
            tokens = _tokenize(chunk["content"] + " " + chunk.get("section", ""))
            self._doc_lens.append(len(tokens))
            total_len += len(tokens)

            tf: dict[str, int] = defaultdict(int)
            for t in tokens:
                tf[t] += 1

            for term, freq in tf.items():
                self._index[term].append((doc_id, freq))

        self._avg_dl = total_len / len(self._chunks) if self._chunks else 1.0
        self._loaded = True

        print(f"[KnowledgeBase] Loaded {len(self._chunks)} chunks from {path}")
        return len(self._chunks)

    # ─── Searching ───────────────────────────────────────────────────────────

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, str, str]]:
        """
        Return top-k (content, url, title) tuples most relevant to the query.
        Returns [] if nothing useful is found or data not loaded.
        """
        if not self._loaded or not self._chunks:
            return []

        query_terms = _tokenize(query)
        if not query_terms:
            return []

        N = len(self._chunks)
        scores: dict[int, float] = defaultdict(float)

        for term in query_terms:
            postings = self._index.get(term)
            if not postings:
                continue

            df = len(postings)
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

            for doc_id, tf in postings:
                dl = self._doc_lens[doc_id]
                norm_tf = (tf * (BM25_K1 + 1)) / (
                    tf + BM25_K1 * (1 - BM25_B + BM25_B * dl / self._avg_dl)
                )
                scores[doc_id] += idf * norm_tf

        if not scores:
            return []

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in ranked[:top_k]:
            if score < MIN_SCORE:
                break
            chunk = self._chunks[doc_id]
            content = chunk["content"].strip()
            url = chunk.get("url", "")
            title = chunk.get("title", chunk.get("section", ""))
            results.append((content, url, title))

        return results

    def search_and_format(self, query: str) -> Optional[str]:
        """
        Search and return a formatted HTML answer string, or None if no good match.
        Called directly by bot_logic.generate_response().
        """
        results = self.search(query, top_k=2)
        if not results:
            return None

        content, url, title = results[0]

        # Extract the most relevant sentences (top 4)
        sentences = re.split(r"(?<=[.!?])\s+", content)
        query_tokens = set(_tokenize(query))

        def sentence_score(s: str) -> int:
            return sum(1 for t in _tokenize(s) if t in query_tokens)

        sentences = sorted(sentences, key=sentence_score, reverse=True)
        answer_text = " ".join(sentences[:4]).strip()

        if len(answer_text) < 40:
            answer_text = content[:600]

        # Build HTML
        source_link = (
            f"<br><br><small><a href='{url}' target='_blank'>Source: {title or url}</a></small>"
            if url else ""
        )

        return f"{answer_text}{source_link}"

    @property
    def is_loaded(self) -> bool:
        return self._loaded and len(self._chunks) > 0


# ─── Singleton ───────────────────────────────────────────────────────────────

kb = KnowledgeBase()
kb.load()
