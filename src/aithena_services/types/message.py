"""Message types for Aithena services."""

from typing import TYPE_CHECKING, Optional, Union, overload

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

    role: Literal["user"] = Field(default="user", frozen=True)
    name: Optional[str] = Field(None, repr=False)
    content: Union[str, list[ContentPart]]  # type: ignore


class SystemMessage(BaseMessage):
    """System message."""

    role: Literal["system"] = Field(default="system", frozen=True)
    content: str  # not optional
    name: Optional[str] = Field(None, repr=False)

    # NOTE: will turn to using prompt as kwarg for Anthropic
    # (and this is the behavior of Gemini by default) so
    # no need for the convert_prompt method


class AssistantMessage(BaseMessage):
    """Assistant message."""

    role: Literal["assistant"] = Field(default="assistant", frozen=True)
    name: Optional[str] = Field(None, repr=False)


class ToolMessage(BaseMessage):
    """Tool message."""

    role: Literal["tool"] = Field(default="tool", frozen=True)


MessageRoot = Annotated[
    Union[UserMessage, SystemMessage, AssistantMessage], Field(discriminator="role")
]


class Message(RootModel):
    """Message for LLM."""

    root: MessageRoot

    if TYPE_CHECKING:

        @overload
        def __init__(self, role: str): ...
        @overload
        def __init__(self, role: str, content: Union[str, list[ContentPart]]): ...
        @overload
        def __init__(
            self, role: str, content: Union[str, list[ContentPart]], name: str
        ): ...

        def __init__(
            self,
            role: str,
            content: Optional[Union[str, list[ContentPart]]] = None,
            name: Optional[str] = None,
        ):  # for mypy compatibility
            root_ = {"role": role, "content": content, "name": name}
            super().__init__(**root_)

    def __getattr__(self, name):
        try:
            return getattr(self.root, name)
        except AttributeError:
            raise AttributeError(  # pylint: disable=W0707
                f"Message has no attribute {name}"
            )

    def __setattr__(self, name, value):
        if name == "root":
            super().__setattr__(name, value)
        else:
            setattr(self.root, name, value)

    def as_dict(self, **kwargs):
        """Wrapper for `self.model_dump(mode="python")`
        with `exclude_unset=True` and `exclude_none=True`.

        Additional keyword arguments are passed to `self.model_dump`.
        If these additional arguments include `exclude_unset` or `exclude_none`,
        these values will be ignored.
        """
        for key in ["exclude_unset", "exclude_none"]:
            if key in kwargs:
                kwargs.pop(key)
        return self.model_dump(
            mode="python", exclude_unset=True, exclude_none=True, **kwargs
        )

    def as_json(self, **kwargs):
        """Wrapper for `self.model_dump(mode="json")`
        with `exclude_unset=True` and `exclude_none=True`.

        Additional keyword arguments are passed to `self.model_dump`.
        If these additional arguments include `exclude_unset` or `exclude_none`,
        these values will be ignored.
        """
        for key in ["exclude_unset", "exclude_none"]:
            if key in kwargs:
                kwargs.pop(key)
        return self.model_dump(
            mode="json", exclude_unset=True, exclude_none=True, **kwargs
        )

    def __repr__(self):
        return f"Message(role={self.root.role}, content={self.root.content})"

    def __str__(self):
        return f"Message(role={self.root.role}, content={self.root.content})"
