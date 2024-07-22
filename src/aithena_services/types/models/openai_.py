"""OpenAI Models."""

from typing import Any, Optional, Union, overload

from openai import OpenAI as OpenAIClient
from openai._streaming import Stream as OpenAIStream
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Literal, Self

from ..message import Message
from .base import BaseLLM


class InternalOpenAIStream(BaseModel):
    """Streamed Response model for OpenAI."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    base_stream: OpenAIStream
    openai_instance: "OpenAI"
    message: Optional[Message] = None

    def __iter__(self):
        msg = ""
        for message in self.base_stream.__iter__():
            content_ = message.choices[0].delta.content
            if content_ is not None:
                msg += content_
            yield message
        self.message = Message(role="assistant", content=msg)
        self.openai_instance.messages.append(self.message)


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


class OpenAI(BaseLLM):
    """OpenAI models."""

    platform: Literal["OpenAI"] = "OpenAI"
    prompt: Optional[Message] = None
    name: Literal[tuple(OPENAI_MODELS)] = "gpt-4o"  # type: ignore
    _stream: Any = None

    @staticmethod
    def list_models() -> list[str]:
        """Wrapper around `list_openai_models`: list available OpenAI chat models."""
        return list_openai_models()

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

    def model_post_init(self, __context: Any):
        self.client = OpenAIClient()

    @property
    def _chat_messages(self):
        msgs_ = [msg.as_json(exclude="name") for msg in self.messages]
        if self.prompt is None:
            return msgs_
        return [self.prompt, *msgs_]

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
            base_stream=self.client.chat.completions.create(
                model=self.name, messages=self._chat_messages, stream=True
            ),
            openai_instance=self,
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
