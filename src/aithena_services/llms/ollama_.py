"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
from typing import Any, Sequence

import requests  # type: ignore
from llama_index.llms.ollama import Ollama as LlamaIndexOllama  # type: ignore

from aithena_services.envvars import OllamaEnv as OLLAMA_URL
from aithena_services.llms.types import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    Message,
)
from aithena_services.llms.utils import check_and_cast_messages


class Ollama(LlamaIndexOllama):
    """Ollama LLMs."""

    def __init__(self, **kwargs: Any):
        kwargs["base_url"] = OLLAMA_URL
        super().__init__(**kwargs)

    @staticmethod
    def list_models(url: str = OLLAMA_URL) -> list[str]:  # type: ignore
        """List available Ollama models."""
        names_ = [
            x["name"]
            for x in requests.get(url + "/api/tags", timeout=40).json()["models"]
        ]
        return [x.replace(":latest", "") for x in names_]

    def chat(self, messages: Sequence[dict | Message], **kwargs: Any) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = super().chat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})

    def stream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().stream_chat(messages, **kwargs)

        def gen() -> ChatResponseGen:

            for response in llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def astream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().astream_chat(messages, **kwargs)

        async def gen() -> ChatResponseAsyncGen:

            async for response in await llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def achat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = await super().achat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})
