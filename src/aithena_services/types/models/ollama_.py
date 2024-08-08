"""Ollama Models."""

import json
import os
from typing import Any, Optional, Union, overload

import requests  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from typing_extensions import Literal

from ..message import Message
from .base import BaseLLM

OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")

if not OLLAMA_URL.endswith("/api"):
    OLLAMA_URL += "/api"
if not OLLAMA_URL.startswith("http"):
    raise ValueError("OLLAMA_URL must start with 'http'")


def list_ollama_models(url: str = OLLAMA_URL) -> list[str]:
    """List available Ollama models."""
    names_ = [
        x["name"] for x in requests.get(url + "/tags", timeout=40).json()["models"]
    ]
    return [x.replace(":latest", "") for x in names_]


OLLAMA_MODELS = list_ollama_models()


class InternalOllamaStream(BaseModel):
    """Streamed Response model for Ollama."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    base_stream: requests.Response
    ollama_instance: "Ollama"
    message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for line in self.base_stream.iter_lines():
            if line:
                js = json.loads(line.decode("utf-8"))
                msg += js["message"]["content"]
                # TODO check if useful 'done_reason' and 'done' in js
            yield line.decode("utf-8")
        self.message = Message(role="assistant", content=msg)
        self.ollama_instance.messages.append(self.message)


# @dataclass
class Ollama(BaseLLM):
    """Ollama models."""

    platform: Literal["Ollama"] = "Ollama"
    name: Literal[tuple(OLLAMA_MODELS)]  # type: ignore
    # prompt: Optional[Message] = None
    base_url: str = Field(default=OLLAMA_URL, frozen=True)
    timeout: int = 40
    _chat_url: str = PrivateAttr()
    _stream: Any = None

    @staticmethod
    def list_models() -> list[str]:
        """List available Ollama models."""
        return list_ollama_models()

    @model_validator(mode="after")
    def validate_messages(self):
        """Validate message list."""
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                self.prompt = message
                self.messages = self.messages[1:]

        self._chat_url = self.base_url + "/chat"
        return self

    @property
    def _chat_json(self):
        if self.prompt is None:
            return {
                "messages": [message.as_json() for message in self.messages],
                "model": self.name,
                "stream": self.stream,
            }
        return {
            "messages": [
                self.prompt.as_json(),
                *[message.as_json() for message in self.messages],
            ],
            "model": self.name,
            "stream": self.stream,
        }

    @overload
    def _send_internal(self, stream: Literal[True]) -> InternalOllamaStream: ...
    @overload
    def _send_internal(self, stream: Literal[False]) -> None: ...

    def _send_internal(self, stream: bool) -> Union[None, InternalOllamaStream]:
        if not stream:
            response = requests.post(
                self._chat_url, json=self._chat_json, timeout=self.timeout
            )
            response_message = Message(response.json()["message"])
            self.messages.append(response_message)
            return None
        # self.stream==True
        self._stream = InternalOllamaStream(
            base_stream=requests.post(
                self._chat_url, json=self._chat_json, stream=True, timeout=self.timeout
            ),
            ollama_instance=self,
        )
        return self._stream

    def send(
        self, message: Optional[Union[Message, str]] = None
    ) -> Union[Message, InternalOllamaStream]:
        """Send a message to the Ollama-served local model.

        If no message is provided, the current message history attached
        to the instance is sent.

        If `self.stream==True`, a stream response is returned. After the
        stream is exhausted, the corresponding `Message` is appended to
        the instance's history.

        If `self.stream==False`, the response `Message` from the model is returned
        and appended to the instance's history.

        Args:
            message: (Optional) The message to send to the model.
        """
        if not self.stream:  # pylint: disable=R1720
            if message is None:
                self._send_internal(self.stream)
                return self.messages[-1]
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            self._send_internal(self.stream)
            return self.messages[-1]
        # self.stream==True
        if message is None:
            return self._send_internal(self.stream)
        if isinstance(message, str):
            message = Message(role="user", content=message)
        self.messages.append(message)
        return self._send_internal(self.stream)
