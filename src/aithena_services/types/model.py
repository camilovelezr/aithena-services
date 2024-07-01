"""LLM Model Types."""

import json
from typing import Any, List, Optional, Union

import requests
from anthropic import Anthropic
from anthropic._streaming import Stream as AnthropicStream
from anthropic.types import TextDelta
from openai import OpenAI as OpenAIClient
from openai._streaming import Stream as OpenAIStream
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Literal, Self

from .message import Message

MODELS = Literal["gpt-4o", "claude-3-5-sonnet-20240620", "ollama"]


@dataclass
class BaseLLM:
    """Base LLM class."""

    name: MODELS
    prompt: Optional[Union[str, Message]] = None
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
    _claude_instance: "Claude"
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


@dataclass
class Claude(BaseLLM):
    """Claude model."""

    prompt: Optional[str] = (
        None  # TODO: check which is better, parameter or User initial message
    )
    name: Literal["claude-3-5-sonnet-20240620"] = "claude-3-5-sonnet-20240620"
    max_tokens: int = 300
    _stream: Any = None

    @model_validator(mode="after")
    def validate_messages(self) -> Self:
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                self.prompt = message.convert_prompt(
                    "gemini"
                )  # TODO TEMPORAL, YES GEMINI HERE
                self.messages = self.messages[1:]
        return self

    def __post_init__(self):
        self.client = Anthropic()

    def _send_internal(self) -> None:
        if not self.stream:
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
        else:  # self.stream==True
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

    def send(self, message: Optional[Union[Message, str]] = None) -> Message:
        if not self.stream:
            if message is None:
                self._send_internal()
                return self.messages[-1]
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            self._send_internal()
            return self.messages[-1]
        else:
            if message is None:
                return self._send_internal()
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            return self._send_internal()


@dataclass(config=ConfigDict(validate_assignment=True))
class OpenAI(BaseLLM):
    """OpenAI models."""

    prompt: Optional[Message] = None
    name: Literal["gpt-4o", "gpt-3.5-turbo"] = "gpt-4o"
    _stream: Any = None

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        if isinstance(value, str):
            return Message(role="system", content=value)
        if isinstance(value, Message):
            return value
        else:
            raise ValueError("prompt must be a string or a Message object")

    @model_validator(mode="after")
    def validate_messages(self):
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                if self.prompt is None:
                    self.prompt = message
                self.messages = self.messages[1:]
            if message.role == "model":
                message.role = "assistant"
        return self

    def __post_init__(self):
        self.client = OpenAIClient()

    @property
    def _chat_messages(self):
        if self.prompt is None:
            return self.messages
        return [self.prompt, *self.messages]

    def _send_internal(self) -> Any:  # TODO: work on Stream Response model
        if not self.stream:
            response = self.client.chat.completions.create(
                model=self.name,
                messages=self._chat_messages,
            )
            response_message = Message(
                role="assistant", content=response.choices[0].message.content
            )
            self.messages.append(response_message)
        else:  # self.stream==True
            self._stream = InternalOpenAIStream(
                self.client.chat.completions.create(
                    model=self.name, messages=self._chat_messages, stream=True
                ),
                self,
            )
            return self._stream

    def send(self, message: Optional[Union[Message, str]] = None) -> Message:
        if not self.stream:  # pylint: disable=R1720
            if message is None:
                self._send_internal()
                return self.messages[-1]
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            self._send_internal()
            return self.messages[-1]
        else:  # self.stream==True
            if message is None:
                return self._send_internal()
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            return self._send_internal()


@dataclass
class Ollama(BaseLLM):
    """Ollama models."""

    model: Optional[str] = None  # since BaseLLM inheritance, this has to have default
    name: Literal["ollama"] = "ollama"
    prompt: Optional[Message] = None
    base_url: str = "http://localhost:11434/api"
    _chat_url: str = Field(init=False)
    _stream: Any = None

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        if isinstance(value, str):
            return Message(role="system", content=value)
        if isinstance(value, Message):
            return value
        else:
            raise ValueError("prompt must be a string or a Message object")

    @model_validator(mode="after")
    def validate_messages(self):
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                self.prompt = message
                self.messages = self.messages[1:]

        if self.model is None:
            raise ValueError("model is required for Ollama.")
        self._chat_url = self.base_url + "/chat"
        return self

    @property
    def _chat_json(self):
        if self.prompt is None:
            return {
                "messages": [message.as_json() for message in self.messages],
                "model": self.model,
                "stream": self.stream,
            }
        return {
            "messages": [
                self.prompt.as_json(),
                *[message.as_json() for message in self.messages],
            ],
            "model": self.model,
            "stream": self.stream,
        }

    def _send_internal(self) -> Any:
        if not self.stream:
            response = requests.post(self._chat_url, json=self._chat_json, timeout=10)
            response_message = Message(response.json()["message"])
            self.messages.append(response_message)
        else:  # self.stream==True
            self._stream = InternalOllamaStream(
                requests.post(
                    self._chat_url, json=self._chat_json, stream=True, timeout=10
                ),
                self,
            )
            return self._stream

    def send(self, message: Optional[Union[Message, str]] = None) -> Message:
        if not self.stream:  # pylint: disable=R1720
            if message is None:
                self._send_internal()
                return self.messages[-1]
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            self._send_internal()
            return self.messages[-1]
        else:  # self.stream==True
            if message is None:
                return self._send_internal()
            if isinstance(message, str):
                message = Message(role="user", content=message)
            self.messages.append(message)
            return self._send_internal()
