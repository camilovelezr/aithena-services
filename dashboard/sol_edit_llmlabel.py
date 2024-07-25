"""Chatbot multiple models."""

# pylint: disable=E1129, E1120, C0116, C0103
import json
from copy import copy
from pathlib import Path
from typing import Any, Type

import reacton.ipyvuetify as rv
import solara
import solara.lab

from aithena_services import BaseLLM, Message  # type: ignore

OPENAI_AVAILABLE = True
ANTHROPIC_AVAILABLE = True
OLLAMA_AVAILABLE = True

try:
    from aithena_services import OpenAI
except ImportError:
    OPENAI_AVAILABLE = False
try:
    from aithena_services import Ollama
except ImportError:
    OLLAMA_AVAILABLE = False
try:
    from aithena_services import Anthropic
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from anthropic.types import TextDelta
except ModuleNotFoundError:
    pass

FILE_PATH = Path(__file__).parent.absolute()

PROMPT = """
You are a helpful assistant named Aithena.
Respond to users with witty, entertaining, and thoughtful answers.
User wants short answers, maximum five sentences.
If user asks info about yourself or your architecture,
respond with info about your LLM model and its capabilities.
Do not finish every sentence with a question.
If you ask a question, always include a question mark.
Do not introduce yourself to user if user does not ask for it.
Never explain to user how your answers are.
"""


def cast_to_message(msg: Any) -> Message:
    """Cast a message to a `Message` object."""
    if not isinstance(msg, (dict, Message)):
        raise ValueError(f"expected a dict or Message object, got {type(msg)}")
    return Message(msg) if not isinstance(msg, Message) else msg


def cast_to_message_list(msgs: list) -> list[Message]:
    """Cast a list of messages to a list of `Message` objects."""
    return [cast_to_message(x) for x in msgs]


messages: solara.Reactive[list[Message]] = solara.reactive(
    ([Message({"role": "system", "content": PROMPT})])
)
OPENAI_MODEL_LIST = []
ANTHROPIC_MODEL_LIST = []
OLLAMA_MODEL_LIST = []


if OPENAI_AVAILABLE:

    def return_openai_model(name: str, prompt: str, stream: bool) -> OpenAI:
        """Return an OpenAI model with the given name, prompt, and stream."""
        return OpenAI(name=name, prompt=prompt, stream=stream)

    OPENAI_MODEL_LIST = OpenAI.list_models()


if ANTHROPIC_AVAILABLE:

    def return_anthropic_model(name: str, prompt: str, stream: bool) -> Anthropic:
        """Return an OpenAI model with the given name, prompt, and stream."""
        return Anthropic(name=name, prompt=prompt, stream=stream)

    ANTHROPIC_MODEL_LIST = Anthropic.list_models()


if OLLAMA_AVAILABLE:

    def return_ollama_model(name: str, prompt: str, stream: bool) -> Ollama:
        """Return an OpenAI model with the given name, prompt, and stream."""
        return Ollama(name=name, prompt=prompt, stream=stream)

    OLLAMA_MODEL_LIST = Ollama.list_models()


LLM_OPTIONS = [*OPENAI_MODEL_LIST, *ANTHROPIC_MODEL_LIST, *OLLAMA_MODEL_LIST]

LLM_DICT = {}

if OPENAI_AVAILABLE:
    LLM_DICT.update(
        {
            name: return_openai_model(name, PROMPT, stream=True)
            for name in OPENAI_MODEL_LIST
        }
    )
if ANTHROPIC_AVAILABLE:
    LLM_DICT.update(
        {
            name: return_anthropic_model(name, PROMPT, stream=True)
            for name in ANTHROPIC_MODEL_LIST
        }
    )
if OLLAMA_AVAILABLE:
    LLM_DICT.update(
        {
            name: return_ollama_model(name, PROMPT, stream=True)
            for name in OLLAMA_MODEL_LIST
        }
    )

LLM_NAME: solara.Reactive[str] = (
    solara.reactive("llama3")
    if "llama3" in LLM_DICT
    else solara.reactive(list(LLM_DICT.keys())[0])
)
LLM: solara.Reactive[Type[BaseLLM]]

RESET_ON_CHANGE: solara.Reactive[bool] = solara.Reactive(False)

EDIT_MODE: solara.Reactive[bool] = solara.Reactive(False)


def add_chunk_to_ai_message(chunk: str):
    """Add chunk to assistant message."""
    messages.value = cast_to_message_list(
        [
            *messages.value[:-1],
            {
                "role": "assistant",
                "content": messages.value[-1].content + chunk,
            },
        ]
    )


def change_llm_name(*args):
    """Change the selected LLM."""
    LLM_NAME.value = args[-1]
    if RESET_ON_CHANGE.value:
        messages.value = cast_to_message_list([{"role": "system", "content": PROMPT}])
        return
    return


def change_reset_value(v):
    """Change the reset_on_change value."""
    RESET_ON_CHANGE.value = v


def change_edit_mode_value(v):
    """Change the edit_mode value."""
    EDIT_MODE.value = v


@solara.component
def ModelRow():
    with solara.Row(
        style={
            "position": "relative",
            "top": "0",
            "width": "100%",
            "height": "38px",
            "padding-left": "12px",
            "padding-right": "12px",
            "padding-top": "15px",
            # "padding": "5px",
        },
    ):
        auto_complete = rv.Autocomplete(
            label="Model", dense=True, items=LLM_OPTIONS, value=LLM_NAME.value
        )
        rv.use_event(auto_complete, "change", change_llm_name)
        solara.Switch(
            label="Reset on Change",
            value=False,
            on_value=change_reset_value,
            style={
                "position": "relative",
                "top": "-8px",
            },
        )
        solara.Switch(
            label="Edit Mode",
            value=False,
            on_value=change_edit_mode_value,
            style={
                "position": "relative",
                "top": "-8px",
            },
        )


edit_index = solara.reactive(None)
current_edit_value = solara.reactive("")


def update_message():
    updated_messages = copy(messages.value)
    updated_messages[edit_index.value] = cast_to_message(
        {
            "role": "assistant",
            "content": current_edit_value.value,
        }
    )
    messages.set(updated_messages)
    edit_index.set(None)


@solara.component
def EditableMessage(message, index):
    def handle_edit():
        edit_index.set(index)
        current_edit_value.set(messages.value[index].content)

    if edit_index.value == index:
        solara.MarkdownEditor(
            value=current_edit_value.value, on_value=current_edit_value.set
        )
        solara.Button(
            "SEND",
            on_click=update_message,
            style={
                "position": "center",
            },
        )
        return

    solara.Markdown(message)
    solara.Button(
        "EDIT",
        on_click=handle_edit,
        style={"position": "center"},
    )
    return


model_labels: solara.Reactive[dict[int, str]] = solara.reactive({})


@solara.component
def ModelButton(index: int, model: str, task, is_last: bool = False):
    if is_last:
        if not task.pending:
            if index not in model_labels.value:
                model_labels.value.update({index: model})
            model_ = model_labels.value[index] if index in model_labels.value else model
            solara.Text(
                model_,
                style={
                    "color": "rgba(0,0,0, 0.5)",
                    "font-size": "0.8em",
                    "position": "relative",
                    "height": "fit-content",
                    "width": "fit-content",
                    "padding-left": "10px",
                },
            )
    else:
        if index not in model_labels.value:
            model_labels.value.update({index: model})
        model_ = model_labels.value[index] if index in model_labels.value else model
        solara.Text(
            model_,
            style={
                "color": "rgba(0,0,0, 0.5)",
                "font-size": "0.8em",
                "position": "relative",
                "height": "fit-content",
                "width": "fit-content",
                "padding-left": "10px",
            },
        )


is_menu_open = solara.reactive(False)


@solara.component
def ChangeModelCard(index: int, model: str):
    def change_llm(*args):
        change_llm_name(*args)
        is_menu_open.set(False)

    with solara.Column(style={"padding": "5px"}):
        solara.Text("Change Model")
        auto_complete = rv.Autocomplete(
            label="Model",
            dense=True,
            items=LLM_OPTIONS,
        )
        rv.use_event(auto_complete, "change", change_llm)


@solara.component
def ModelLabel(index: int, model: str, task, is_last: bool = False):
    if is_last:
        if not task.pending:
            with solara.Row(
                gap="0px",
                style={
                    "position": "relative",
                    "width": "fit-content",
                    "top": "-2",
                    "height": "auto",
                },
            ):
                with solara.Div(
                    style={
                        "position": "relative",
                        "width": "fit-content",
                    }
                ):

                    ModelButton(index, model, task, is_last)
                    btn = rv.Btn(
                        children=[
                            rv.Icon(
                                children=["mdi-head-plus"],
                            )
                        ],
                        icon=True,
                    )
                    with solara.lab.Menu(
                        activator=btn,
                        close_on_content_click=False,
                        open_value=is_menu_open,
                        on_open_value=is_menu_open.set,
                    ):
                        ChangeModelCard(index, model)
                    # rv.use_event(btn, "click", handle_click)
    else:
        with solara.Row(
            gap="0px",
            style={
                "position": "relative",
                "width": "fit-content",
                "top": "-2",
                "height": "auto",
            },
        ):
            with solara.Div(
                style={
                    "position": "relative",
                    "width": "fit-content",
                }
            ):
                ModelButton(index, model, task, is_last)
                rv.Btn(
                    children=[
                        rv.Icon(
                            children=["mdi-head-plus"],
                        )
                    ],
                    icon=True,
                )


@solara.component
def Page():
    solara.Style(FILE_PATH.joinpath("style.css"))
    solara.Title("Aithena")
    CURRENT_LLM: solara.Reactive[BaseLLM] = solara.reactive(  # type: ignore
        LLM_DICT[LLM_NAME.value]
    )
    if CURRENT_LLM.value.platform == "Ollama":
        CURRENT_LLM.value.prompt = messages.value[0]
    else:
        CURRENT_LLM.value.prompt = PROMPT
    CURRENT_LLM.value.messages = messages.value[1:]

    user_message_count = len([m for m in messages.value if m.role == "user"])

    def user_send(message):
        messages.value = cast_to_message_list(
            [
                *messages.value,
                {"role": "user", "content": message},
            ]
        )

        CURRENT_LLM.messages = messages.value[1:]

    def call_llm():
        if user_message_count == 0:
            return
        response = CURRENT_LLM.value.send()
        messages.value = cast_to_message_list(
            [*messages.value, {"role": "assistant", "content": ""}]
        )
        if OPENAI_AVAILABLE and isinstance(CURRENT_LLM.value, OpenAI):
            for chunk in response:
                if chunk.choices[0].finish_reason == "stop":
                    return
                add_chunk_to_ai_message(chunk.choices[0].delta.content)  # type: ignore
        if ANTHROPIC_AVAILABLE and isinstance(CURRENT_LLM.value, Anthropic):
            for chunk in response:
                if hasattr(chunk, "delta") and isinstance(chunk.delta, TextDelta):
                    msg = chunk.delta.text
                    add_chunk_to_ai_message(msg)
        if OLLAMA_AVAILABLE and isinstance(CURRENT_LLM.value, Ollama):
            for chunk in response:
                if chunk:
                    add_chunk_to_ai_message(json.loads(chunk)["message"]["content"])

    task = solara.lab.use_task(call_llm, dependencies=[user_message_count])  # type: ignore

    with solara.Column(
        style={
            "width": "100%",
            "position": "relative",
            "height": "calc(100vh - 50px)",
            "padding-bottom": "15px",
            "overflow-y": "auto",
        },
    ):
        ModelRow()
        with solara.lab.ChatBox():
            for index, item in enumerate(CURRENT_LLM.value.messages):
                is_last = index == len(CURRENT_LLM.value.messages) - 1
                if item.role == "system":
                    continue
                with solara.Column(gap="0px"):
                    with solara.Div(style={"background-color": "rgba(0,0,0.3, 0.06)"}):
                        with solara.lab.ChatMessage(
                            user=item.role == "user",
                            avatar=False,
                            name="Aithena" if item.role == "assistant" else "User",
                            color=(
                                "rgba(0,0,0, 0.06)"
                                if item.role == "assistant"
                                else "#ff991f"
                            ),
                            avatar_background_color=(
                                "primary" if item.role == "assistant" else None
                            ),
                            border_radius="20px",
                            style={
                                "padding": "10px",
                            },
                        ):
                            if EDIT_MODE.value and item.role == "assistant":
                                EditableMessage(
                                    item.content, index + 1
                                )  # add 1 to index to account for prompt
                            else:
                                solara.Markdown(item.content)
                    if item.role == "assistant":
                        ModelLabel(index, CURRENT_LLM.value.name, task, is_last)
        solara.lab.ChatInput(
            send_callback=user_send,
            disabled=task.pending,
            style={
                "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "padding-bottom": "5px",
            },
        )
