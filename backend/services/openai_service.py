from openai import OpenAI
from typing import Union

from core.config import settings

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GROK_MODEL = "llama-3.3-70b-versatile"


def _get_client_and_model() -> tuple[OpenAI, str]:
    """
    Returns an OpenAI-compatible client and the model name for Groq.
    """
    api_key = settings.openai_api_key
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    base_url = settings.openai_base_url
    model_name = settings.openai_model or DEFAULT_OPENAI_MODEL

    # Detect if key looks like a Groq API key
    if api_key.startswith("gsk_"):
        if not base_url:
            base_url = "https://api.groq.com/openai/v1"
        if model_name == DEFAULT_OPENAI_MODEL:
            model_name = DEFAULT_GROK_MODEL

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model_name


def ask_openai(prompt_or_messages: Union[str, list[dict]]) -> str:
    """
    Sends a user prompt to the AI service and returns the response.
    """
    if not settings.openai_api_key:
        print("OpenAI service warning: OPENAI_API_KEY is not configured.")
        return ""

    try:
        client, model_name = _get_client_and_model()
        if isinstance(prompt_or_messages, list):
            messages = prompt_or_messages
        else:
            messages = [{"role": "user", "content": prompt_or_messages}]

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.2,
        )
        text = (response.choices[0].message.content or "").strip()
        print("[OPENAI/GROQ] response received")
        return text
    except Exception as exc:
        print("OpenAI service error:", exc)
        return ""
