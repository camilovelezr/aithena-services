# mypy: disable-error-code="import-untyped"
"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
from typing import Any, Sequence

from llama_index.llms.azure_openai import AzureOpenAI as LlamaIndexAzureOpenAI

from aithena_services.envvars import (
    AZURE_OPENAI_API_VERSION_ENV as AZURE_OPENAI_API_VERSION,
)
from aithena_services.envvars import (
    AZURE_OPENAI_DEPLOYMENT_NAME_ENV as AZURE_OPENAI_DEPLOYMENT_NAME,
)
from aithena_services.envvars import AZURE_OPENAI_ENDPOINT_ENV as AZURE_OPENAI_ENDPOINT
from aithena_services.envvars import AZURE_OPENAI_KEY_ENV as AZURE_OPENAI_KEY
from aithena_services.envvars import AZURE_OPENAI_MODEL_ENV as AZURE_OPENAI_MODEL
from aithena_services.llms.types import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    Message,
)
from aithena_services.llms.utils import check_and_cast_messages


class AzureOpenAI(LlamaIndexAzureOpenAI):
    """AzureOpenAI LLMs."""

    def __init__(self, **kwargs: Any):
        kwargs["api_key"] = AZURE_OPENAI_KEY
        kwargs["azure_endpoint"] = AZURE_OPENAI_ENDPOINT
        kwargs["api_version"] = AZURE_OPENAI_API_VERSION
        if AZURE_OPENAI_MODEL is not None:
            kwargs["model"] = AZURE_OPENAI_MODEL
        if AZURE_OPENAI_DEPLOYMENT_NAME is not None:
            kwargs["engine"] = AZURE_OPENAI_DEPLOYMENT_NAME
        super().__init__(**kwargs)

    # @staticmethod
    # def list_models(url: str = OLLAMA_URL) -> list[str]:  # type: ignore
    #     """List available Ollama models."""
    #     names_ = [
    #         x["name"]
    #         for x in requests.get(url + "/api/tags", timeout=40).json()["models"]
    #     ]
    #     return [x.replace(":latest", "") for x in names_]

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
