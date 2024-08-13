"""Aithena Services."""

from aithena_services.envvars import (
    AnthropicAvailable,
    OllamaAvailable,
    OpenAIAvailable,
)

from .types import BaseLLM, Message

__all__ = ["Message", "BaseLLM"]

if OpenAIAvailable:
    from .types import OpenAI

    __all__.append("OpenAI")

if AnthropicAvailable:
    from .types import Anthropic

    __all__.append("Anthropic")

if OllamaAvailable:
    from .types import Ollama

    __all__.append("Ollama")
