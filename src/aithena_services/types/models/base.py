"""Base class for LLM Models."""

from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Literal

from ..message import Message


def _prompt_to_message(value: Union[str, Message]) -> Message:
    """Convert prompt to SystemMessage if str."""
    if isinstance(value, str):
        return Message(role="system", content=value)
    if isinstance(value, Message):
        return value
    raise ValueError("prompt must be a string or a Message object")


# @dataclass
class BaseLLM(BaseModel):
    """Base LLM class."""

    name: str = Field(..., description="The name of the LLM model to use.")
    platform: Literal["OpenAI", "Anthropic", "Ollama"] = Field(init=False, frozen=True)
    prompt: Optional[Message] = None
    messages: list[Message] = Field(default_factory=list)
    client: Any = None
    stream: bool = False

    def __setattr__(self, name: str, value: Any):
        """Set attribute."""
        if name == "prompt":
            value = _prompt_to_message(value)
        super().__setattr__(name, value)

    @field_validator("prompt", mode="before")
    @classmethod
    def check_prompt(cls, value):
        """Validate prompt."""
        return _prompt_to_message(value)
