"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors, W1203
import logging
from typing import Any, Sequence

import requests  # type: ignore
from llama_index.llms.ollama import Ollama as LlamaIndexOllama  # type: ignore

from aithena_services.envvars import OLLAMA_HOST as OLLAMA_URL
from aithena_services.llms.types import Message
from aithena_services.llms.types.base import (
    AithenaLLM,
    achataithena,
    astreamchataithena,
    chataithena,
    streamchataithena,
)
from aithena_services.llms.types.response import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
)

logger = logging.getLogger("aithena_services.llms.ollama")


# TODO: check how to set multiple stop sequences, because Ollama supports it
class Ollama(LlamaIndexOllama, AithenaLLM):
    """Ollama LLMs.

    To use this, you must first deploy a model on Ollama.

    You must have the following environment variables set:

    OLLAMA_HOST: url for the Ollama server, e.g.
       http://localhost:11434

    Args:
        model: name of the model (e.g. `llama3.1`)
        request_timeout: timeout for the request in seconds, default is 30
        temperature: temperature for sampling, higher values => more creative answers

            0 ≤ temperature ≤ 1.0

        context_window: maximum number of tokens to consider in the context, default is 3900
        ...

    For a full list of parameters, visit
    [Ollama Docs](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values)

    """

    def __init__(self, **kwargs: Any):
        kwargs["base_url"] = OLLAMA_URL
        logger.debug(f"Initalizing Ollama with kwargs: {kwargs}")
        super().__init__(**kwargs)

    @staticmethod
    def list_models(url: str = OLLAMA_URL) -> list[str]:  # type: ignore
        """List available Ollama models."""
        return [
            x["name"]
            for x in requests.get(url + "/api/tags", timeout=40).json()["models"]
        ]

    @chataithena
    def chat(self, messages: Sequence[dict | Message], **kwargs: Any) -> ChatResponse:
        """Chat with a model in Ollama.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().chat(messages, **kwargs)  # type: ignore

    @streamchataithena
    def stream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseGen:
        """Stream chat with a model in Ollama.

        Each response is a `ChatResponse` and has a `.delta`
        attribute useful for incremental updates.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().stream_chat(messages, **kwargs)  # type: ignore

    @achataithena
    async def achat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponse:
        """Async chat with a model in Ollama.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().achat(messages, **kwargs)  # type: ignore

    @astreamchataithena
    async def astream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        """Async stream chat with a model in Ollama.

        Each response is a `ChatResponse` and has a `.delta`
        attribute useful for incremental updates.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().astream_chat(messages, **kwargs)  # type: ignore
