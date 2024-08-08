"""LLM Models for Aithena Services."""

from aithena_services.envvars import (
    AnthropicAvailable,
    OllamaAvailable,
    OpenAIAvaliable,
)

from .base import BaseLLM

__all__ = ["BaseLLM"]


if OpenAIAvaliable:
    from .openai_ import OpenAI

    __all__.append("OpenAI")

if AnthropicAvailable:
    from .anthropic_ import Anthropic

    __all__.append("Anthropic")

if OllamaAvailable:
    from .ollama_ import Ollama

    __all__.append("Ollama")
