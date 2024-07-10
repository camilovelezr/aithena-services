"""LLM Model Types."""

import json
import os
from typing import Any, List, Optional, Union, get_type_hints, overload

import requests  # type: ignore
from anthropic import Anthropic as AnthropicClient
from anthropic._streaming import Stream as AnthropicStream
from anthropic.types import TextDelta
from openai import OpenAI as OpenAIClient
from openai._streaming import Stream as OpenAIStream
from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Literal, Self

from .message import Message


@dataclass
class BaseLLM:
    """Base LLM class."""

    name: str
    platform: Literal["OpenAI", "Anthropic", "Ollama"] = Field(init=False, frozen=True)
    prompt: Optional[Message] = None
    messages: List[Message] = Field(default_factory=list)
    client: Any = None
    stream: bool = False


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class InternalOpenAIStream:
    """Streamed Response model for OpenAI."""

    _base_stream: OpenAIStream
    _openai_instance: "OpenAI"
    _message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for message in self._base_stream.__iter__():
            content_ = message.choices[0].delta.content
            if content_ is not None:
                msg += content_
            yield message
        self._message = Message(role="assistant", content=msg)
        self._openai_instance.messages.append(self._message)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class InternalClaudeStream:
    """Streamed Response model for Claude."""

    _base_stream: AnthropicStream
    _claude_instance: "Anthropic"
    _message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for message in self._base_stream.__iter__():
            if hasattr(message, "delta") and isinstance(message.delta, TextDelta):
                msg += message.delta.text
            yield message
        self._message = Message(role="assistant", content=msg)
        self._claude_instance.messages.append(self._message)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class InternalOllamaStream:
    """Streamed Response model for Ollama."""

    _base_stream: requests.Response
    _ollama_instance: "Ollama"
    _message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for line in self._base_stream.iter_lines():
            if line:
                js = json.loads(line.decode("utf-8"))
                msg += js["message"]["content"]
                # TODO check if useful 'done_reason' and 'done' in js
            yield line.decode("utf-8")
        self._message = Message(role="assistant", content=msg)
        self._ollama_instance.messages.append(self._message)


ANTHROPIC_MODELS = get_type_hints(AnthropicClient().messages.create)["model"].__args__[
    1
]


@dataclass
class Anthropic(BaseLLM):
    """Anthropic model."""

    platform: Literal["Anthropic"] = "Anthropic"
    name: ANTHROPIC_MODELS = "claude-3-5-sonnet-20240620"  # type: ignore
    max_tokens: int = 300
    _stream: Any = None

    @staticmethod
    def list_models() -> List[str]:
        """Wrapper around `ANTHROPIC_MODELS`: list available Anthropic models."""
        return list(ANTHROPIC_MODELS.__args__)

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        """Validate prompt."""
        if isinstance(value, str):
            return Message(role="user", content=f"<instructions>{value}</instructions>")
        if isinstance(value, Message):
            return value.convert_prompt("claude")
        raise ValueError("prompt must be a string or a SystemMessage object")

    @model_validator(mode="after")
    def validate_messages(self) -> Self:
        """Validate message list."""
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                self.prompt = message.convert_prompt("claude")
                self.messages = self.messages[1:]
        return self

    def __post_init__(self):
        self.client = AnthropicClient()

    @overload
    def _send_internal(self, stream: Literal[True]) -> InternalClaudeStream: ...
    @overload
    def _send_internal(self, stream: Literal[False]) -> None: ...

    def _send_internal(self, stream: bool) -> Union[None, InternalClaudeStream]:
        if not stream:
            response = self.client.messages.create(
                model=self.name,
                max_tokens=self.max_tokens,
                system=self.prompt,
                messages=self.messages,
            )
            response_message = Message(
                role="assistant", content=response.content[0].text
            )
            self.messages.append(response_message)
            return None
        # stream=True
        self._stream = InternalClaudeStream(
            self.client.messages.create(
                model=self.name,
                max_tokens=self.max_tokens,
                system=self.prompt,
                messages=self.messages,
                stream=True,
            ),
            self,
        )
        return self._stream

    def send(
        self, message: Optional[Union[Message, str]] = None
    ) -> Union[Message, InternalClaudeStream]:
        """Send a message to the Anthropic model.

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
        if not self.stream:
            if message is None:
                self._send_internal(self.stream)
                return self.messages[-1]
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            self._send_internal(self.stream)
            return self.messages[-1]
        # stream=True
        if message is None:
            return self._send_internal(self.stream)
        if isinstance(message, str):
            message = Message(role="user", content=message)
        self.messages.append(message)
        return self._send_internal(self.stream)


def custom_sort_for_openai_models(name: str) -> tuple[int, str]:
    """Custom sort function for OpenAI models."""
    return int(name.split("-")[1].split(".")[0][0]), name  # gpt-3.5 -> (3, "gpt-3.5")


def list_openai_models() -> list[str]:
    """List available OpenAI models."""
    return sorted(
        [
            x.id
            for x in OpenAIClient().models.list().data
            if "gpt" in x.id and "instruct" not in x.id
        ],
        key=custom_sort_for_openai_models,
        reverse=True,
    )


OPENAI_MODELS = list_openai_models()


@dataclass
class OpenAI(BaseLLM):
    """OpenAI models."""

    platform: Literal["OpenAI"] = "OpenAI"
    prompt: Optional[Message] = None
    name: Literal[tuple(OPENAI_MODELS)] = "gpt-4o"  # type: ignore
    _stream: Any = None

    @staticmethod
    def list_models() -> List[str]:
        """Wrapper around `list_openai_models`: list available OpenAI chat models."""
        return list_openai_models()

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        """Validate prompt."""
        if isinstance(value, str):
            return Message(role="system", content=value)
        if isinstance(value, Message):
            return value
        else:
            raise ValueError("prompt must be a string or a Message object")

    @model_validator(mode="after")
    def validate_messages(self) -> Self:
        """Validate message list."""
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                if self.prompt is None:
                    self.prompt = message
                self.messages = self.messages[1:]
            if message.role == "model":
                message.role = "assistant"  # type: ignore
        return self

    def __post_init__(self):
        self.client = OpenAIClient()

    @property
    def _chat_messages(self):
        if self.prompt is None:
            return self.messages
        return [self.prompt, *self.messages]

    @overload
    def _send_internal(self, stream: Literal[True]) -> InternalOpenAIStream: ...
    @overload
    def _send_internal(self, stream: Literal[False]) -> None: ...

    def _send_internal(self, stream: bool) -> Union[None, InternalOpenAIStream]:
        if not stream:
            response = self.client.chat.completions.create(
                model=self.name,
                messages=self._chat_messages,
            )
            response_message = Message(
                role="assistant", content=response.choices[0].message.content
            )
            self.messages.append(response_message)
            return None
        # stream=True
        self._stream = InternalOpenAIStream(
            self.client.chat.completions.create(
                model=self.name, messages=self._chat_messages, stream=True
            ),
            self,
        )
        return self._stream

    def send(
        self, message: Optional[Union[Message, str]] = None
    ) -> Union[Message, InternalOpenAIStream]:
        """Send a message to the OpenAI model.

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
        if message is None:
            return self._send_internal(self.stream)
        if isinstance(message, str):
            message = Message(role="user", content=message)
        self.messages.append(message)
        return self._send_internal(self.stream)


OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")

if not OLLAMA_URL.endswith("/api"):
    OLLAMA_URL += "/api"
if not OLLAMA_URL.startswith("http"):
    raise ValueError("OLLAMA_URL must start with 'http'")


def list_ollama_models(url: str = OLLAMA_URL) -> List[str]:
    """List available Ollama models."""
    names_ = [
        x["name"] for x in requests.get(url + "/tags", timeout=10).json()["models"]
    ]
    return [x.replace(":latest", "") for x in names_]


OLLAMA_MODELS = list_ollama_models()


@dataclass
class Ollama(BaseLLM):
    """Ollama models."""

    platform: Literal["Ollama"] = "Ollama"
    name: Literal[tuple(OLLAMA_MODELS)]  # type: ignore
    # prompt: Optional[Message] = None
    base_url: str = Field(default=OLLAMA_URL, frozen=True)
    _chat_url: str = Field(init=False)
    _stream: Any = None

    @staticmethod
    def list_models() -> List[str]:
        """List available Ollama models."""
        return list_ollama_models()

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        """Validate prompt."""
        if isinstance(value, str):
            return Message(role="system", content=value)
        if isinstance(value, Message):
            return value
        else:
            raise ValueError("prompt must be a string or a Message object")

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
            response = requests.post(self._chat_url, json=self._chat_json, timeout=10)
            response_message = Message(response.json()["message"])
            self.messages.append(response_message)
            return None
        # self.stream==True
        self._stream = InternalOllamaStream(
            requests.post(
                self._chat_url, json=self._chat_json, stream=True, timeout=10
            ),
            self,
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
