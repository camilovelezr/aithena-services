"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
import logging
from typing import Any, Sequence

import requests  # type: ignore
from docstring_inheritance import inherit_google_docstring
from llama_index.llms.ollama import Ollama as LlamaIndexOllama  # type: ignore

from aithena_services.envvars import OLLAMA_HOST_ENV as OLLAMA_URL
from aithena_services.llms.types import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    Message,
)
from aithena_services.llms.utils import check_and_cast_messages

logger = logging.getLogger("aithena_services.llms.ollama")


# TODO: check how to set multiple stop sequences, because Ollama supports it
class Ollama(LlamaIndexOllama):
    """Ollama LLMs.

    To use this, you must first deploy a model on Ollama.

    You must have the following environment variables set:

    OLLAMA_URL: url for the Ollama server, e.g.
       http://localhost:11434

    Args:
        model: name of the model (e.g. `llama3.1`)
        request_timeout: timeout for the request in seconds, default is 30
        temperature: temperature for sampling, higher values => more creative answers

            0 ≤ temperature ≤ 1.0

        context_window: maximum number of tokens to consider in the context, default is 3900
        repeat_last_n: sets how far back for the model to look back to prevent repetition,
            default is 64. 0=disabled, -1=context_window
        repeat_penalty: sets how strongly to penalize repetitions.
            Higher values (e.g 1.5) => stronger penalty.
            Lower values (e.g 0.9) => more lenient, default is 1.1
        seed: set random number seed used for generation. Setting this to a specific
            value will make the model generate reproducible results, default is 0
        mirostat: enable Mirostat sampling for controlling perplexity,
            default is 0, 0=disabled, 1=Mirostat, 2=Mirostat 2.0
        mirostat_eta: how quickly the algorithm responds to feedback from the generated text.
            Lower learning rate => slower adjustments, default is 0.1
        mirostat_tau: balance between coherence and diversity of the output.
            Lower value => more focused and coherent text, default is 5.0
        stop: set the stop sequence. When this pattern is encountered, the LLM will
            stop generating text and return.
        tfs_z: tail free sampling. Used to reduce the impact of less probable tokens from
            the output. Higher values (e.g 2.0) => greater reduction of impact. Value of
            1.0 disables this setting, default is 1.0
        top_k: reduces the probability of generating nonsense.
            Higher values (e.g 100) => more diverse answers.
            Lower values (e.g 10) => more conservative, default is 40
        top_p: works together with top_k. Higher values (e.g 0.95) => more diverse answers.
            Lower values (e.g 0.5) => more conservative and focused, default is 0.9
        min_p: alternative to top_p. Aims to ensure a balance of quality and variety.
            The parameter p represents the minimum probability of a token to be considered,
            relative to the probability of the most likely token. For example, if p=0.05 and the
            most likely token has a probability of 0.9, logits witha a value less than p*0.9=0.045
            are filtered out, default is 0.0




    """

    def __init__(self, **kwargs: Any):
        kwargs["base_url"] = OLLAMA_URL
        logger.debug(f"Initalizing Ollama with kwargs: {kwargs}")
        super().__init__(**kwargs)

    @staticmethod
    def list_models(url: str = OLLAMA_URL) -> list[str]:  # type: ignore
        """List available Ollama models."""
        names_ = [
            x["name"]
            for x in requests.get(url + "/api/tags", timeout=40).json()["models"]
        ]
        return [x.replace(":latest", "") for x in names_]

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


inherit_google_docstring(LlamaIndexOllama.__doc__, Ollama)
