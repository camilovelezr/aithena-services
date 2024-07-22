"""Anthropic Models."""

from typing import Any, Optional, Union, get_type_hints, overload

from anthropic import Anthropic as AnthropicClient
from anthropic._streaming import Stream as AnthropicStream
from anthropic.types import TextDelta
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Literal, Self

from ..message import Message
from .base import BaseLLM

ANTHROPIC_MODELS = get_type_hints(AnthropicClient().messages.create)["model"].__args__[
    1
]


class InternalClaudeStream(BaseModel):
    """Streamed Response model for Claude."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    base_stream: AnthropicStream
    anthropic_instance: "Anthropic"
    message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for message in self.base_stream.__iter__():
            if hasattr(message, "delta") and isinstance(message.delta, TextDelta):
                msg += message.delta.text
            yield message
        self.message = Message(role="assistant", content=msg)
        self.anthropic_instance.messages.append(self.message)


class Anthropic(BaseLLM):
    """Anthropic model."""

    platform: Literal["Anthropic"] = "Anthropic"
    name: ANTHROPIC_MODELS = "claude-3-5-sonnet-20240620"  # type: ignore
    max_tokens: int = 300
    _stream: Any = None

    @staticmethod
    def list_models() -> list[str]:
        """Wrapper around `ANTHROPIC_MODELS`: list available Anthropic models."""
        return list(ANTHROPIC_MODELS.__args__)

    @property
    def _chat_messages(self):
        msgs_ = [msg.as_json(exclude="name") for msg in self.messages]
        return msgs_

    @property
    def _prompt(self):
        return self.prompt.content

    @model_validator(mode="after")
    def validate_messages(self) -> Self:
        """Validate message list."""
        for n, message in enumerate(self.messages):
            if n == 0 and message.role == "system":
                self.messages = self.messages[1:]
        return self

    def model_post_init(self, __context: Any):
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
                system=self._prompt,
                messages=self._chat_messages,
            )
            response_message = Message(
                role="assistant", content=response.content[0].text
            )
            self.messages.append(response_message)
            return None
        # stream=True
        self._stream = InternalClaudeStream(
            base_stream=self.client.messages.create(
                model=self.name,
                max_tokens=self.max_tokens,
                system=self._prompt,
                messages=self._chat_messages,
                stream=True,
            ),
            anthropic_instance=self,
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
