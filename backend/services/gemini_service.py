# backend/services/gemini_service.py
from google import genai
from core.config import settings

MODEL_NAME = "gemini-2.0-flash"

# Create client once (safe to do at import time)
client = genai.Client(api_key=settings.gemini_api_key)

def ask_gemini(prompt: str) -> str:
    try:
        # DEBUG: log prompt for debugging language issues
        print("[GEMINI] prompt:\n" + prompt)
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        # resp.text is usually present; fallback just in case
        text = getattr(resp, "text", None) or str(resp)
        print("[GEMINI] raw response:\n" + text)
        return text
    except Exception as e:
        # log so it's visible when quota or other errors happen
        print("Gemini service error:", e)
        # return empty string (caller will fall back to other logic)
        return ""