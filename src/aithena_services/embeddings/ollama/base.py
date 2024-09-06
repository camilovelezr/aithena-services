# mypy: disable-error-code="import-untyped"
# pylint: disable=too-many-ancestors
"""Ollama Embeddings based on LlamaIndex."""

from typing import Any

from llama_index.embeddings.ollama import OllamaEmbedding as LlamaIndexOllama

from aithena_services.envvars import OLLAMA_HOST as OLLAMA_URL


class OllamaEmbedding(LlamaIndexOllama):
    """Ollama embeddings."""

    def __init__(self, **kwargs: Any):
        if "model_name" not in kwargs:
            if "model" not in kwargs:
                raise ValueError("Model not specified.")
            kwargs["model_name"] = kwargs["model"]
        if "base_url" not in kwargs:
            kwargs["base_url"] = OLLAMA_URL
        super().__init__(**kwargs)
