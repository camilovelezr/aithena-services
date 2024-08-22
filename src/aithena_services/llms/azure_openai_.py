# mypy: disable-error-code="import-untyped"
"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
from typing import Any, Sequence

from llama_index.llms.azure_openai import AzureOpenAI as LlamaIndexAzureOpenAI

from aithena_services.envvars import AZURE_OPENAI_ENV_DICT
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


class AzureOpenAI(LlamaIndexAzureOpenAI, AithenaLLM):
    """Azure OpenAI LLMs.

    To use this, you must first deploy a model on Azure OpenAI.
    Unlike OpenAI, you need to specify a `engine` parameter to identify
    your deployment (called "model deployment name" in Azure portal).
    You must have the following environment variables set:

    - `AZURE_OPENAI_API_VERSION`: set this to `2023-07-01-preview` or newer.
        This may change in the future.
    - `AZURE_OPENAI_ENDPOINT`: your endpoint should look like the following
        https://YOUR_RESOURCE_NAME.openai.azure.com/
    - `AZURE_OPENAI_API_KEY`: your API key

    Args:
        model: Name of the model (e.g. `gpt-4o-mini`)
        deployment: This will correspond to the custom name you chose
            for your deployment when you deployed a model.
            Alias: `engine`.

    """

    @staticmethod
    def list_models() -> list[str]:
        """List available models/deployments in Azure OpenAI.

        This method is not implemented in Azure OpenAI.
        The API calls needed for this, require elevated permissions
        and are not part of Azure OpenAI REST API.
        """
        raise NotImplementedError(
            "list_models() is not yet implemented in Azure OpenAI."
        )

    def __init__(self, **kwargs: Any):
        kwargs["api_key"] = AZURE_OPENAI_ENV_DICT["api_key"]
        kwargs["azure_endpoint"] = AZURE_OPENAI_ENV_DICT["endpoint"]
        kwargs["api_version"] = AZURE_OPENAI_ENV_DICT["api_version"]
        if "deployment" in kwargs:
            if "engine" in kwargs:
                raise ValueError("Cannot specify both `deployment` and `engine`.")
            kwargs["engine"] = kwargs["deployment"]
            kwargs.pop("deployment")
        super().__init__(**kwargs)

    @chataithena
    def chat(self, messages: Sequence[dict | Message], **kwargs: Any) -> ChatResponse:
        """Chat with a model in Azure OpenAI.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().chat(messages, **kwargs)  # type: ignore

    @streamchataithena
    def stream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseGen:
        """Stream chat with a model in Azure OpenAI.

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
        """Async chat with a model in Azure OpenAI.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().achat(messages, **kwargs)  # type: ignore

    @astreamchataithena
    async def astream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        """Async stream chat with a model in Azure OpenAI.

        Each response is a `ChatResponse` and has a `.delta`
        attribute useful for incremental updates.

        Args:
            messages: entire list of message history, where last
                message is the one to be responded to
        """
        return super().astream_chat(messages, **kwargs)  # type: ignore
