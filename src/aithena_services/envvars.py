"""Environment Variable Configuration for Aithena Services."""

import os

OpenAIEnv = os.getenv("OPENAI_API_KEY", None)
AnthropicEnv = os.getenv("ANTHROPIC_API_KEY", None)
OllamaEnv = os.getenv("OLLAMA_URL", None)

OpenAIAvailable = OpenAIEnv is not None
AnthropicAvailable = AnthropicEnv is not None
OllamaAvailable = OllamaEnv is not None


__all__ = [
    "OpenAIAvailable",
    "AnthropicAvailable",
    "OllamaAvailable",
    "OpenAIEnv",
    "AnthropicEnv",
    "OllamaEnv",
]
