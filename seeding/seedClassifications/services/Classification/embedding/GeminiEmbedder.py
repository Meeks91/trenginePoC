

from __future__ import annotations

import google.generativeai as genai


EMBEDDING_MODEL = "models/gemini-embedding-2-preview"


class GeminiEmbedder:


    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)

    # ── API ──

    def embed(self, text: str) -> list[float]:
        """Embed a single text string."""
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
        )
        return result["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts in one call."""
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
        )
        return result["embedding"]
