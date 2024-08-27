# mypy: disable-error-code="import-untyped"
"""Aithena-Services FastAPI REST Endpoints. """

# pylint: disable=W1203, C0412

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from funcs import add_model_to_config, add_ollama_models_to_config
from models import ChatModel, init_models

from aithena_services.envvars import (
    AZURE_OPENAI_AVAILABLE,
    OLLAMA_AVAILABLE,
    OPENAI_AVAILABLE,
)

# OPENAI_AVAILABLE = False
# AZURE_OPENAI_AVAILABLE = False

if OPENAI_AVAILABLE:
    from aithena_services.llms.openai import OpenAI
if AZURE_OPENAI_AVAILABLE:
    from aithena_services.llms.azure_openai import AzureOpenAI
if OLLAMA_AVAILABLE:
    from aithena_services.llms.ollama import Ollama


app = FastAPI()


Models = init_models()


def check_platform(platform: str):
    """Check if the platform is valid."""
    if platform not in ["ollama", "openai", "azure"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid platform, must be 'ollama', 'openai' or 'azure'",
        )
    if platform == "ollama" and not OLLAMA_AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="Ollama is not available.",
        )
    if platform == "openai" and not OPENAI_AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="OpenAI is not available.",
        )
    if platform == "azure" and not AZURE_OPENAI_AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="Azure OpenAI is not available.",
        )


# @app.get("/chat/list")
# def list_models():
#     """List all available chat models."""
#     models = []
#     if OLLAMA_AVAILABLE:
#         models.extend(Ollama.list_models())
#     if OPENAI_AVAILABLE:
#         models.extend(OpenAI.list_models())
#     # if AZURE_OPENAI_AVAILABLE:
#     #     models.extend([f"azure/{AZURE_OPENAI_MODEL_ENV}"])
#     return models


@app.get("/chat/list")
def list_models():
    """List all available chat models."""
    return Models.names


@app.get("/chat/list/{platform}")
def list_models_by_platform(platform: str):
    """List all available chat models by platform."""
    check_platform(platform)
    return [model.name for model in Models.filter_models(platform)]


@app.post("/chat/list")
def add_model_to_list(model_dict: dict):
    """Add model to config"""
    try:
        add_model_to_config(model_dict)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.put("/chat/list/update")
def update_models():
    """Update models."""
    Models.update()


@app.put("/chat/list/update/ollama")
def update_ollama_models():
    """Update Ollama models."""

    add_ollama_models_to_config()
    Models.update()


# @app.get("/chat/list/{platform}")
# def list_models_by_platform(platform: str):
#     """List all available chat models by platform."""
#     print(f"checking platform {platform}")
#     check_platform(platform)
#     if platform == "ollama":
#         return Ollama.list_models()
#     if platform == "openai":
#         return OpenAI.list_models()
#     if platform == "azure":
#         raise HTTPException(
#             status_code=400,
#             detail="Azure OpenAI does not have an implemented list_models.",
#         )
#     # if platform == "azure":
#     #     return [f"azure/{AZURE_OPENAI_MODEL_ENV}"]
#     raise HTTPException(  # just for readability, check_platform should raise
#         status_code=400,
#         detail="Invalid platform, must be 'ollama', 'openai' or 'azure'",
#     )
# TODO: override url for ollama


def get_client(model: ChatModel):
    """Get client for model."""
    if model.backend == "ollama":
        return Ollama(model=model.model, base_url=str(model.config.url))
    if model.backend == "openai":
        return OpenAI(
            model=model.model,
            api_key=model.config.api_key,
            api_base=model.config.api_base,
        )
    if model.backend == "azure":
        return AzureOpenAI(
            api_key=model.config.api_key,
            azure_endpoint=str(model.config.endpoint),
            api_version=model.config.api_version,
            model=model.model,
            deployment=model.config.deployment,
        )
    raise HTTPException(
        status_code=400,
        detail="Invalid platform, must be 'ollama', 'openai' or 'azure'",
    )


@app.post("/chat/{model}/generate")
async def generate_from_msgs(
    model: str,
    messages: list[dict],
    stream: bool = True,
):
    """Generate a chat completion from a list of messages."""

    print(f"For {model} chat, received {messages}, stream: {stream}")
    model_ = Models.get_model(model)
    backend = model_.backend
    check_platform(backend)
    client = get_client(model_)

    if stream:

        async def stream_response(messages):
            async for chunk in await client.astream_chat(messages):
                # print(chunk, type(chunk))
                response = chunk.__dict__
                # print(f"response is {response}")
                response["message"] = chunk.message.root.model_dump_json()
                yield json.dumps(response, default=lambda x: x.model_dump_json()) + "\n"

        return StreamingResponse(
            stream_response(messages), media_type="application/json"
        )
    return await client.achat(messages)
