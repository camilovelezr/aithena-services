"""LLM Models for Aithena Services."""

from aithena_services.envvars import OllamaAvailable, OpenAIAvaliable
from aithena_services.llms.types import Message

__all__ = ["Message"]
if OpenAIAvaliable:
    from .openai_ import OpenAI

    __all__.append("OpenAI")

# if AnthropicAvailable:
#     from .anthropic_ import Anthropic

#     __all__.append("Anthropic")

if OllamaAvailable:
    from .ollama_ import Ollama

    __all__.append("Ollama")
