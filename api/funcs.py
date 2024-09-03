# mypy: disable-error-code="import-untyped"
"""Functions for Aithena Services API."""

import json
from copy import copy
from pathlib import Path

import requests
from models import ChatModel

from aithena_services.envvars import OLLAMA_AVAILABLE

if OLLAMA_AVAILABLE:
    from aithena_services.envvars import OLLAMA_HOST as OLLAMA_URL

CONFIG_PATH = Path(__file__).parent / "config.json"


def _get_current_models() -> tuple[list[dict], list[str]]:
    """Get current models in config.json and return (list[dict], list[str]).

    The first list is a list of ChatModels as `dict`, the second list is
    a list of the model names, equivalent to doing `x["name"] for x in firstlist`.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        current_models = json.load(file)["models"]
    current_names = [x["name"] for x in current_models]
    return current_models, current_names


def _write_to_config_json(data: dict) -> None:
    """Write data to config.json."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def _ollama_result_to_model_obj(res: dict) -> ChatModel:
    """Convert Ollama API result to ChatModel object."""
    # mypy complains no 'params'
    return ChatModel(  # type: ignore
        name=res["name"],
        model=res["model"],
        backend="ollama",
        config={"url": OLLAMA_URL},
    )


def get_models_from_ollama() -> list[ChatModel]:
    """Retrieve list of models from Ollama."""
    res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=40).json()["models"]
    names = [model["name"] for model in res]
    names = [name for name in names if not "embed" in name]
    models = [model["model"] for model in res]
    models = [model for model in models if not "embed" in model]
    if len(names) < 1:
        return []
    return [
        _ollama_result_to_model_obj({"name": name, "model": model})
        for name, model in zip(names, models)
    ]


def add_ollama_models_to_config(overwrite: bool = False) -> None:
    """Scan local Ollama models and add to config.

    Args:
        overwrite: if `False`, a model with the same name as one
            that is already present in config.json will be ignored

    """
    current_models, current_names = _get_current_models()
    ollama: dict[str, list] = {"models": []}
    ollama["models"].extend(
        [json.loads(x.model_dump_json()) for x in get_models_from_ollama()]
    )
    data: dict[str, list] = {"models": copy(current_models)}
    for model in ollama["models"]:
        if not overwrite:
            if model["name"] not in current_names:
                data["models"].append(model)
        else:
            data["models"].append(model)
    _write_to_config_json(data)


def add_model_to_config(model_dict: dict) -> None:
    """Add new model to config.json"""
    chat_model = ChatModel(**model_dict)
    current_models, current_names = _get_current_models()
    if chat_model.name in current_names:
        raise ValueError("Model name already in config.json")
    current_models.append(json.loads(chat_model.model_dump_json()))
    data: dict = {"models": current_models}
    _write_to_config_json(data)