"""Message types for Aithena services."""

# from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field, RootModel
from typing_extensions import Annotated, Literal


class BaseMessage(BaseModel):
    """Base class for all messages."""

    role: Literal["user", "system", "assistant", "tool"]
    content: Optional[str] = None


# OpenAI
class BaseContentPart(BaseModel):
    """Base class for content parts."""

    type: Literal["text", "image_url"]


class ContentPartText(BaseContentPart):
    """Content part with text."""

    type: Literal["text"]
    text: str


class ImageUrl(BaseModel):
    """Image URL with optional detail level."""

    url: str
    detail: Literal["auto", "low", "high"] = "auto"


class ContentPartImage(BaseContentPart):
    """Content part with image URL."""

    type: Literal["image_url"]
    image_url: ImageUrl


ContentPart = Annotated[
    Union[ContentPartText, ContentPartImage], Field(discriminator="type")
]


class UserMessage(BaseMessage):
    """User message."""

    role: Literal["user"] = "user"
    name: Optional[str] = Field(None, repr=False)
    content: Union[str, list[ContentPart]]


class SystemMessage(BaseMessage):
    """System message."""

    role: Literal["system"] = "system"
    content: str  # not optional
    name: Optional[str] = Field(None, repr=False)


class AssistantMessage(BaseMessage):
    """Assistant message."""

    role: Literal["assistant"] = "assistant"
    name: Optional[str] = Field(None, repr=False)


class ToolMessage(BaseMessage):
    """Tool message."""

    role: Literal["tool"] = "tool"


MessageRoot = Annotated[
    Union[UserMessage, SystemMessage, AssistantMessage], Field(discriminator="role")
]


class Message(RootModel):
    """Message for LLM."""

    root: MessageRoot

    def __getattr__(self, name):
        try:
            return getattr(self.root, name)
        except AttributeError:
            raise AttributeError(  # pylint: disable=W0707
                f"Message has no attribute {name}"
            )

    def as_dict(self):
        """Wrapper for `self.model_dump(mode="python")`"""
        return self.model_dump(mode="python", exclude_unset=True, exclude_none=True)

    def as_json(self):
        """Wrapper for `self.model_dump(mode="json")`"""
        return self.model_dump(mode="json", exclude_unset=True, exclude_none=True)

    def __repr__(self):
        return f"Message({self.root})"

    def __str__(self):
        return f"Message({self.root})"

    def convert_prompt(  # pylint: disable=R1710
        self, model: Literal["claude", "gemini"]
    ) -> Union["Message", str]:
        """Create a `UserMessage` with the given prompt as content.

        This is for Claude. The format is <instructions> ```prompt```</instructions>.
        """
        if self.role != "system":
            raise ValueError("only SystemMessages can be converted")
        if model not in {"claude", "gemini"}:
            raise ValueError(f"model must be 'claude' or 'gemini', not {model}")
        if model == "claude":
            return Message(  # type: ignore
                role="user", content=f"<instructions>{self.content}</instructions>"
            )
        if model == "gemini":
            return self.content
