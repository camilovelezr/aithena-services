"""OpenAI Implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
from typing import Any, Sequence

from llama_index.llms.openai import OpenAI as LlamaIndexOpenAI  # type: ignore
from openai import OpenAI as OpenAIClient

from aithena_services.llms.types import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    Message,
)
from aithena_services.llms.utils import check_and_cast_messages


def custom_sort_for_openai_models(name: str) -> tuple[int, str]:
    """Custom sort function for OpenAI models."""
    return int(name.split("-")[1].split(".")[0][0]), name  # gpt-3.5 -> (3, "gpt-3.5")


def list_openai_models() -> list[str]:
    """List available OpenAI models."""
    return sorted(
        [
            x.id
            for x in OpenAIClient().models.list().data
            if "gpt" in x.id and "instruct" not in x.id
        ],
        key=custom_sort_for_openai_models,
        reverse=True,
    )


OPENAI_MODELS = list_openai_models()


class OpenAI(LlamaIndexOpenAI):
    """OpenAI models."""

    @staticmethod
    def list_models() -> list[str]:
        """List available OpenAI chat models."""
        return list_openai_models()

    def chat(self, messages: Sequence, **kwargs: Any) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = super().chat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})

    def stream_chat(self, messages: Sequence, **kwargs: Any) -> ChatResponseGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().stream_chat(messages, **kwargs)

        def gen() -> ChatResponseGen:

            for response in llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def astream_chat(
        self, messages: Sequence, **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().astream_chat(messages, **kwargs)

        async def gen() -> ChatResponseAsyncGen:

            async for response in await llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def achat(self, messages: Sequence, **kwargs: Any) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = await super().achat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})
