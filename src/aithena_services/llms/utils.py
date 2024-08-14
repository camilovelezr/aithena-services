"""LLM Utils."""

from typing import Sequence

from aithena_services.llms.types import Message


def cast_messages(messages: Sequence) -> Sequence[Message]:
    """Cast dict messages to Message."""
    return [Message(**x) for x in messages]


def check_messages(messages: Sequence) -> bool:
    """Check messages."""
    return all(isinstance(x, Message) for x in messages) or all(
        isinstance(x, dict) for x in messages
    )


def check_and_cast_messages(messages: Sequence) -> Sequence[Message]:
    """Check and cast messages."""
    if not check_messages(messages):
        raise ValueError("Messages must be a sequence of type Message or dict.")
    if all(isinstance(x, dict) for x in messages):
        messages = cast_messages(messages)
    return messages
