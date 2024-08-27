"""Pydantic Models for Aithena-Services FastAPI REST Endpoints."""

import json
from pathlib import Path
from typing import Literal, Optional, Self, Set, TypeVar

from pydantic import BaseModel, Field, HttpUrl, model_validator

CONFIG_PATH = Path(__file__).with_name("config.json")


class AzureOpenAIConfig(BaseModel):
    """Azure OpenAI Config."""

    api_key: str
    endpoint: HttpUrl
    api_version: str
    deployment: str


class OpenAIConfig(BaseModel):
    """OpenAI Config."""

    api_key: str
    api_base: Optional[HttpUrl] = None


class OllamaConfig(BaseModel):
    """Ollama Config."""

    url: HttpUrl


Config = TypeVar("Config", AzureOpenAIConfig, OpenAIConfig, OllamaConfig)


class InvalidConfigError(Exception):
    """Invalid config error."""


class ChatModel(BaseModel):
    """ChatModel Config Pydantic Class."""

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


class ModelsClass(BaseModel):
    """Models class."""

    models: list[ChatModel]
    names: Set[str]

    def filter_models(self, platform: str):
        """Filter models by platform."""
        return [model for model in self.models if model.backend == platform]

    def update(self):
        """Update from config."""
        self.models, self.names = read_model_config()

    def get_model(self, name: str):
        """Get model by name."""
        return [model for model in self.models if model.name == name][0]


def read_model_config():
    """Read model list from config."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        model_list = json.load(f)["models"]
    models = [ChatModel(**model) for model in model_list]
    names = [model.name for model in models]
    return models, names


def init_models():
    """Initialize model list from config.json."""
    list_, names_ = read_model_config()
    return ModelsClass(models=list_, names=names_)
