"""Aithena Services Types."""

# pylint: disable=W0718

from aithena_services.envvars import (
    AnthropicAvailable,
    OllamaAvailable,
    OpenAIAvaliable,
)

from .message import Message
from .models import BaseLLM

__all__ = ["Message", "BaseLLM"]

if OpenAIAvaliable:
    from .models import OpenAI

    __all__.append("OpenAI")

if AnthropicAvailable:
    from .models import Anthropic

    __all__.append("Anthropic")

if OllamaAvailable:
    from .models import Ollama

    __all__.append("Ollama")
