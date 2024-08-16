# mypy: disable-error-code="import-untyped"
"""Aithena-Services FastAPI REST Endpoints. """

# pylint: disable=W1203, C0412

import json
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from aithena_services.envvars import (
    AZURE_OPENAI_AVAILABLE,
    OLLAMA_AVAILABLE,
    OPENAI_AVAILABLE,
)
from aithena_services.llms.types import Message

if OPENAI_AVAILABLE:
    from aithena_services.llms import OpenAI
if AZURE_OPENAI_AVAILABLE:
    from aithena_services.envvars import AZURE_OPENAI_MODEL_ENV
    from aithena_services.llms import AzureOpenAI
if OLLAMA_AVAILABLE:
    from aithena_services.llms import Ollama

app = FastAPI()


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


@app.get("/chat/list")
def list_models():
    """List all available chat models."""
    models = []
    if OLLAMA_AVAILABLE:
        models.extend(Ollama.list_models())
    if OPENAI_AVAILABLE:
        models.extend(OpenAI.list_models())
    if AZURE_OPENAI_AVAILABLE:
        models.extend([f"azure/{AZURE_OPENAI_MODEL_ENV}"])
    return models


@app.get("/chat/list/{platform}")
def list_models_by_platform(platform: str):
    """List all available chat models by platform."""
    print(f"checking platform {platform}")
    check_platform(platform)
    if platform == "ollama":
        return Ollama.list_models()
    if platform == "openai":
        return OpenAI.list_models()
    if platform == "azure":
        return [f"azure/{AZURE_OPENAI_MODEL_ENV}"]
    raise HTTPException(  # just for readability, check_platform should raise
        status_code=400,
        detail="Invalid platform, must be 'ollama', 'openai' or 'azure'",
    )


@app.post("/chat/azure/generate")
async def generate_azure(
    messages: list[dict],
    stream: bool = True,
    deployment: Optional[str] = None,
    model: Optional[str] = None,
):
    """Generate a chat completion from a list of messages.

    Args:
        messages: List of messages.
        stream: Stream the response.
        deployment: Optional name of the deployment, will override env var.
        model: Optional name of the model, will override env var.
    """
    check_platform("azure")
    print(f"For Azure chat, received {messages}, stream: {stream}")
    messages_ = [Message(**msg) for msg in messages]
    if deployment is not None and model is not None:
        model_ = AzureOpenAI(engine=deployment, model=model)
    elif deployment is not None:
        model_ = AzureOpenAI(engine=deployment)
    elif model is not None:
        model_ = AzureOpenAI(model=model)
    else:
        model_ = AzureOpenAI()
    if stream:

        async def stream_response(messages_):
            async for chunk in await model_.astream_chat(messages_):
                print(chunk, type(chunk))
                response = chunk.dict()
                print(f"response is {response}")
                response["message"] = chunk.message.root.model_dump_json()
                yield json.dumps(response, default=lambda x: x.dict()) + "\n"

        return StreamingResponse(
            stream_response(messages_), media_type="application/json"
        )
    return await model_.achat(messages_)


@app.post("/chat/{model}/generate")
async def generate_from_msgs(model: str, messages: list[dict], stream: bool = True):
    """Generate a chat completion from a list of messages."""
    if OLLAMA_AVAILABLE:
        ollama_models = Ollama.list_models()
    if OPENAI_AVAILABLE:
        openai_models = OpenAI.list_models()
    print(f"For {model} chat, received {messages}, stream: {stream}")
    messages_ = [Message(**msg) for msg in messages]
    if OLLAMA_AVAILABLE and model in ollama_models:
        model_ = Ollama(model=model)
    elif OPENAI_AVAILABLE and model in openai_models:
        model_ = OpenAI(model=model)
    else:
        raise HTTPException(status_code=400, detail="Invalid model.")

    if stream:

        async def stream_response(messages_):
            async for chunk in await model_.astream_chat(messages_):
                # print(chunk, type(chunk))
                response = chunk.dict()
                # print(f"response is {response}")
                response["message"] = chunk.message.root.model_dump_json()
                yield json.dumps(response, default=lambda x: x.dict()) + "\n"

        return StreamingResponse(
            stream_response(messages_), media_type="application/json"
        )
    return await model_.achat(messages_)
