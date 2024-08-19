"""Chatbot multiple models."""

# pylint: disable=E1129, E1120, C0116, C0103
import json
from copy import copy
from pathlib import Path
from typing import Any, Type

import reacton.ipyvuetify as rv
import solara
import solara.lab

from aithena_services.envvars import (
    AZURE_OPENAI_AVAILABLE,
    OLLAMA_AVAILABLE,
    OPENAI_AVAILABLE,
)

if AZURE_OPENAI_AVAILABLE:
    from aithena_services.envvars import AZURE_OPENAI_MODEL_ENV
    from aithena_services.llms import AzureOpenAI
if OPENAI_AVAILABLE:
    from aithena_services.llms import OpenAI
if OLLAMA_AVAILABLE:
    from aithena_services.llms import Ollama

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


messages: solara.Reactive[list[dict]] = solara.reactive(
    ([{"role": "system", "content": PROMPT}])
)

LLMS_AVAILABLE = []
if AZURE_OPENAI_AVAILABLE:
    LLMS_AVAILABLE.append(f"azure/{AZURE_OPENAI_MODEL_ENV}")
if OPENAI_AVAILABLE:
    LLMS_AVAILABLE.extend(OpenAI.list_models())
if OLLAMA_AVAILABLE:
    LLMS_AVAILABLE.extend(Ollama.list_models())


def get_model(name: str):
    if AZURE_OPENAI_AVAILABLE and name.startswith("azure/"):
        return AzureOpenAI()
    if OPENAI_AVAILABLE and name in OpenAI.list_models():
        return OpenAI(model=name)
    if OLLAMA_AVAILABLE and name in Ollama.list_models():
        return Ollama(model=name)


LLM_DICT = {name: get_model(name) for name in LLMS_AVAILABLE}


LLM_NAME: solara.Reactive[str] = (
    solara.reactive("llama3.1")
    if "llama3.1" in LLM_DICT
    else solara.reactive(list(LLM_DICT.keys())[0])
)

RESET_ON_CHANGE: solara.Reactive[bool] = solara.Reactive(False)

EDIT_MODE: solara.Reactive[bool] = solara.Reactive(False)


def add_chunk_to_ai_message(chunk: str):
    """Add chunk to assistant message."""
    messages.value = [
        *messages.value[:-1],
        {
            "role": "assistant",
            "content": messages.value[-1]["content"] + chunk,
        },
    ]


def change_llm_name(*args):
    """Change the selected LLM."""
    LLM_NAME.value = args[-1]
    if RESET_ON_CHANGE.value:
        messages.value = [{"role": "system", "content": PROMPT}]
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
            label="Model", dense=True, items=LLMS_AVAILABLE, value=LLM_NAME.value
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
    updated_messages[edit_index.value] = {
        "role": "assistant",
        "content": current_edit_value.value,
    }

    messages.set(updated_messages)
    edit_index.set(None)


@solara.component
def EditableMessage(message, index):
    def handle_edit():
        edit_index.set(index)
        current_edit_value.set(messages.value[index]["content"])

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
            items=LLMS_AVAILABLE,
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
                                children=["mdi-creation"],
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
                            children=["mdi-creation"],
                        )
                    ],
                    icon=True,
                )


@solara.component
def Page():
    solara.Style(FILE_PATH.joinpath("style.css"))
    solara.Title("Aithena")
    CURRENT_LLM: solara.Reactive = solara.reactive(  # type: ignore
        LLM_DICT[LLM_NAME.value]
    )

    user_message_count = len([m for m in messages.value if m["role"] == "user"])

    def user_send(message):
        messages.value = [
            *messages.value,
            {"role": "user", "content": message},
        ]

    def call_llm():
        if user_message_count == 0:
            return
        response = CURRENT_LLM.value.stream_chat(messages=messages.value)
        messages.value = [
            *messages.value,
            {"role": "assistant", "content": ""},
        ]
        for chunk in response:
            if chunk:
                add_chunk_to_ai_message(chunk.delta)

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
            for index, item in enumerate(messages.value):
                is_last = index == len(messages.value) - 1
                if item["role"] == "system":
                    continue
                if item["content"] == "":
                    continue
                with solara.Column(gap="0px"):
                    with solara.Div(style={"background-color": "rgba(0,0,0.3, 0.06)"}):
                        with solara.lab.ChatMessage(
                            user=item["role"] == "user",
                            avatar=False,
                            name="Aithena" if item["role"] == "assistant" else "User",
                            color=(
                                "rgba(0,0,0, 0.06)"
                                if item["role"] == "assistant"
                                else "#ff991f"
                            ),
                            avatar_background_color=(
                                "primary" if item["role"] == "assistant" else None
                            ),
                            border_radius="20px",
                            style={
                                "padding": "10px",
                            },
                        ):
                            if EDIT_MODE.value and item["role"] == "assistant":
                                EditableMessage(item["content"], index)
                            else:
                                solara.Markdown(item["content"])
                    if item["role"] == "assistant":
                        if CURRENT_LLM.value.class_name == "azure_openai_llm":
                            ModelLabel(
                                index,
                                f"azure/{CURRENT_LLM.value.engine}",
                                task,
                                is_last,
                            )
                        else:
                            ModelLabel(index, CURRENT_LLM.value.model, task, is_last)
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
