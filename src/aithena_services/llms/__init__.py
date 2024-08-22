"""LLM Models for Aithena Services."""

from aithena_services.envvars import (
    AZURE_OPENAI_AVAILABLE,
    OLLAMA_AVAILABLE,
    OPENAI_AVAILABLE,
)

__all__ = []
if OPENAI_AVAILABLE:
    from .openai_ import OpenAI

    __all__.append("OpenAI")

if AZURE_OPENAI_AVAILABLE:
    from .azure_openai_ import AzureOpenAI

    __all__.append("AzureOpenAI")

if OLLAMA_AVAILABLE:
    from .ollama_ import Ollama

    __all__.append("Ollama")
