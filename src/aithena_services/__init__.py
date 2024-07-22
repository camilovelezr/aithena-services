"""Aithena Services."""

import os

from .types import BaseLLM, Message

__all__ = ["Message", "BaseLLM"]

if os.getenv("OPENAI_API_KEY") is not None:
    from .types import OpenAI

    __all__.append("OpenAI")

if os.getenv("ANTHROPIC_API_KEY") is not None:
    from .types import Anthropic

    __all__.append("Anthropic")

if os.getenv("OLLAMA_URL") is not None:
    from .types import Ollama

    __all__.append("Ollama")
