"""LLM Models for Aithena Services."""

import os

from .base import BaseLLM

__all__ = ["BaseLLM"]

if os.getenv("OPENAI_API_KEY", None) is not None:
    from .openai_ import OpenAI

    __all__.append("OpenAI")

if os.getenv("ANTHROPIC_API_KEY", None) is not None:
    from .anthropic_ import Anthropic

    __all__.append("Anthropic")

if os.getenv("OLLAMA_URL", None) is not None:
    from .ollama_ import Ollama

    __all__.append("Ollama")
