"""Pydantic Models for Aithena-Services FastAPI REST Endpoints."""

import json
from typing import Literal, Optional, Self, Set, TypeVar

from pydantic import BaseModel, Field, HttpUrl, model_validator
from utils import CONFIG_PATH, _write_to_config_json


class AzureOpenAIConfig(BaseModel):
    """Azure OpenAI Config."""

    endpoint: HttpUrl
    api_version: str
    deployment: str


class OpenAIConfig(BaseModel):
    """OpenAI Config."""

    api_base: Optional[HttpUrl] = None


class OllamaConfig(BaseModel):
    """Ollama Config."""

    url: HttpUrl


Config = TypeVar("Config", AzureOpenAIConfig, OpenAIConfig, OllamaConfig)


class InvalidConfigError(Exception):
    """Invalid config error."""


class EmbedModel(BaseModel):
    """EmbedModel Config Pydantic Class."""

    name: str
    model: str
    backend: Literal["ollama", "openai", "azure"]
    # mypy complains, pydantic ok:
    config: Config  # type: ignore
    params: Optional[dict] = Field(
        default=None,
        description="Model parameters like temperature.",
    )

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        """Validate config."""
        if self.backend == "ollama" and not isinstance(self.config, OllamaConfig):
            raise InvalidConfigError("Invalid config for Ollama model.")
        if self.backend == "openai" and not isinstance(self.config, OpenAIConfig):
            raise InvalidConfigError("Invalid config for OpenAI model.")
        if self.backend == "azure" and not isinstance(self.config, AzureOpenAIConfig):
            raise InvalidConfigError("Invalid config for Azure OpenAI model.")
        return self

    def as_dict(self):
        """Return model as dict."""
        return json.loads(self.model_dump_json())


class EmbedModels(BaseModel):
    """Models class."""

    models: list[EmbedModel]
    names: Set[str]

    def filter_models(self, platform: str):
        """Filter models by platform."""
        return [model for model in self.models if model.backend == platform]

    def update(self):
        """Update from config."""
        self.models, self.names = read_embed_model_config()

    def get_model(self, name: str):
        """Get model by name."""
        filtered = [model for model in self.models if model.name == name]
        if len(filtered) == 1:
            return filtered[0]
        else:
            raise ValueError(f"Model {name} not found.")

    def delete_model(self, name: str):
        """Delete model by name."""
        self.models = [model for model in self.models if model.name != name]
        self.names = {model.name for model in self.models}
        _write_to_config_json({"embed_models": [x.as_dict() for x in self.models]})


def read_embed_model_config():
    """Read embed model list from config."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        model_list = json.load(f)["embed_models"]
    models = [EmbedModel(**model) for model in model_list]
    names = [model.name for model in models]
    return models, names


def init_embed_models():
    """Initialize model list from config.json."""
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write('{"chat_models": [], "embed_models": []}')
    list_, names_ = read_embed_model_config()
    return EmbedModels(models=list_, names=names_)


# TODO: handle repeated keys => should not be allowed
