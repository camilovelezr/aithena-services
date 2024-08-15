"""LLM Models for Aithena Services."""

from aithena_services.envvars import (
    AZURE_OPENAI_AVAILABLE,
    OLLAMA_AVAILABLE,
    OPENAI_AVAILABLE,
)
from aithena_services.llms.types import Message

__all__ = ["Message"]
if OPENAI_AVAILABLE:
    from .openai_ import OpenAI

    __all__.append("OpenAI")

if AZURE_OPENAI_AVAILABLE:
    from .azure_openai_ import AzureOpenAI

    __all__.append("AzureOpenAI")

if OLLAMA_AVAILABLE:
    from .ollama_ import Ollama

    __all__.append("Ollama")
