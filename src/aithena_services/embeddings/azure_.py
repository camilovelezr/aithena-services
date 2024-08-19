# pylint: disable=R0901
# mypy: disable-error-code="import-untyped"
"""Azure OpenAI Embeddings based on LlamaIndex."""

from llama_index.embeddings.azure_openai import (
    AzureOpenAIEmbedding as LlamaIndexAzureOpenAI,
)

from aithena_services.envvars import AZURE_OPENAI_ENV_DICT


class AzureOpenAIEmbedding(LlamaIndexAzureOpenAI):
    """Azure OpenAI embeddings."""

    def __init__(self, name: str, **kwargs):  # name is alias for azure_deployment
        kwargs["api_key"] = AZURE_OPENAI_ENV_DICT["api_key"]
        kwargs["api_version"] = AZURE_OPENAI_ENV_DICT["api_version"]
        kwargs["azure_deployment"] = name
        super().__init__(**kwargs)
