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
    from aithena_services.llms import AzureOpenAI
if OLLAMA_AVAILABLE:
    from aithena_services.llms import Ollama

app = FastAPI()


def check_platform(platform: str):
    """Check if the platform is valid."""
    if platform not in ["ollama", "openai"]:
        raise HTTPException(
            status_code=400, detail="Invalid platform, must be 'ollama' or 'openai'"
        )


@app.get("/chat/list")
def list_models():
    """List all available chat models."""
    ollama_models = Ollama.list_models()
    openai_models = OpenAI.list_models()
    return ollama_models + openai_models


@app.get("/chat/list/{platform}")
def list_models_by_platform(platform: str):
    """List all available chat models by platform."""
    check_platform(platform)
    ollama_models = Ollama.list_models()
    openai_models = OpenAI.list_models()
    return {"ollama": ollama_models, "openai": openai_models}[platform]


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
    print(f"For {model} chat, received {messages}, stream: {stream}")
    messages_ = [Message(**msg) for msg in messages]
    ollama_models = Ollama.list_models()
    openai_models = OpenAI.list_models()
    if model in ollama_models:
        model_ = Ollama(model=model)
    elif model in openai_models:
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
