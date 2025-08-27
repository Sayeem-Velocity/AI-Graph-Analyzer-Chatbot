from __future__ import annotations
import base64
import mimetypes
from typing import Iterable, Optional

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Restrict to your two models
SCOUT = "meta-llama/llama-4-scout-17b-16e-instruct"
MAVERICK = "meta-llama/llama-4-maverick-17b-128e-instruct"
DEFAULT_MODEL = SCOUT

# Short, simple system prompt for graph analysis + title
SYSTEM_PROMPT = (
    "You are a careful graph analyst. Only use what is clearly visible in the image "
    "(and any user text). Start your answer with a concise, neutral Title for the graph "
    "on the first line. Then provide a human-like explanation in plain English: what the "
    "figure shows, axes/units if visible, main trend(s), peaks/valleys, and 2–4 bullet "
    "highlights with approximate numbers using '≈' when needed. If labels or scales are "
    "unclear/cropped, say so briefly. Keep it objective and concise."
    "generate a proper explanation of the graph within 2000 tokens , a good and concise and overall explanation"
    "If you don't see a graph, say 'No graph detected'."
    "Generate a proper description of the graph"
)

def _to_data_url(image_bytes: bytes, filename: str | None) -> str:
    """Convert raw image bytes to a data URL usable as image_url."""
    mime, _ = mimetypes.guess_type(filename or "")
    if mime is None:
        mime = "image/png"
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

class ImageChatAgent:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL, system_prompt: str = SYSTEM_PROMPT):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt

    def build_messages(self, user_text: str, image_data_url: Optional[str]) -> list[dict]:
        content = []
        if user_text:
            content.append({"type": "text", "text": user_text})
        if image_data_url:
            content.append({"type": "image_url", "image_url": {"url": image_data_url}})
        if not content:
            raise ValueError("You must provide text or an image.")
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content},
        ]

    def stream(self, user_text: str, image_bytes: Optional[bytes], filename: Optional[str]) -> Iterable[str]:
        image_url = _to_data_url(image_bytes, filename) if image_bytes else None
        messages = self.build_messages(user_text, image_url)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_completion_tokens=2951,
            top_p=0.2,
            stream=True,
            stop=None,
        )
        for chunk in completion:
            yield chunk.choices[0].delta.content or ""

    def complete(self, user_text: str, image_bytes: Optional[bytes], filename: Optional[str]) -> str:
        image_url = _to_data_url(image_bytes, filename) if image_bytes else None
        messages = self.build_messages(user_text, image_url)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_completion_tokens=8192,
            top_p=0.2,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content or ""
