"""Chatbot multiple models."""

# pylint: disable=E1129, E1120, C0116, C0103
import json
from copy import copy
from pathlib import Path

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

from llama_index.core.llms.llm import LLM

FILE_PATH = Path(__file__).parent.absolute()

# keep track of all available models
LLMS_AVAILABLE = []
if AZURE_OPENAI_AVAILABLE:
    LLMS_AVAILABLE.append(f"azure/{AZURE_OPENAI_MODEL_ENV}")
if OPENAI_AVAILABLE:
    LLMS_AVAILABLE.extend(OpenAI.list_models())
if OLLAMA_AVAILABLE:
    LLMS_AVAILABLE.extend(Ollama.list_models())


def create_llm(name: str):
    """Create a model client for a given model configuration
    Configuration are defined through environment variables in aithena services.
    ."""
    if AZURE_OPENAI_AVAILABLE and name.startswith("azure/"):
        return AzureOpenAI()
    if OPENAI_AVAILABLE and name in OpenAI.list_models():
        return OpenAI(model=name)
    if OLLAMA_AVAILABLE and name in Ollama.list_models():
        return Ollama(model=name)


"""Retrieve all available models.
TODO this should probably be part of the services API
since aithena-services act as a gateway to all models.
"""
LLM_DICT = {name: create_llm(name) for name in LLMS_AVAILABLE}


"""LLM currently selected."""
LLM_NAME: solara.Reactive[str] = (
    solara.reactive("llama3.1")
    if "llama3.1" in LLM_DICT
    else solara.reactive(list(LLM_DICT.keys())[0])
)


"""history will be erased on model change."""
RESET_ON_CHANGE: solara.Reactive[bool] = solara.Reactive(False)


"""Make all assistant reponse editable."""
# TODO not sure how useful it is, as the previous conversation may
# become inconsitent.
EDIT_MODE: solara.Reactive[bool] = solara.Reactive(False)

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

# global state : we kept track of message history
# we initialize history with the system prompt
messages: solara.Reactive[list[dict]] = solara.reactive(
    ([{"role": "system", "content": PROMPT}])
)
edit_index = solara.reactive(None)
current_edit_value = solara.reactive("")
model_labels: solara.Reactive[dict[int, str]] = solara.reactive({})
is_menu_open = solara.reactive(False)
# LLM selected 
current_llm: solara.Reactive[LLM] = solara.reactive(  # type: ignore
    LLM_DICT[LLM_NAME.value]
)
user_message_count = len([m for m in messages.value if m["role"] == "user"])

@solara.component
def ChatOptions():
    """Chat Options Component.
    
    We can currently:
    - select a specific llms depending on configured sources.
    - edit llms responses
    - reset history on model change.
    """

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

    # anchor at the top-level
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

@solara.component
def EditableMessage(message, index):
    """Display edit options for a 'message' at a given 'index'."""

    def update_message_history():
        """Update the message history with the edited message."""
        updated_messages = copy(messages.value)
        updated_messages[edit_index.value] = {
            "role": "assistant",
            "content": current_edit_value.value,
        }
        messages.set(updated_messages)
        edit_index.set(None)

    def handle_edit():
        """Handle click on the edit button for a given message."""
        edit_index.set(index)
        current_edit_value.set(messages.value[index]["content"])

    with solara.Column() as main:
        
        if edit_index.value == index:
            # The message is currently being edited.
            solara.MarkdownEditor(
                value=current_edit_value.value, on_value=current_edit_value.set
            )
            solara.Button(
                "Done",
                on_click=update_message_history,
                style={
                    "position": "center",
                },
            )
        else:
            # we provide option to edit the message.
            solara.Markdown(message)
            solara.Button(
                "EDIT",
                on_click=handle_edit,
                style={"position": "center"},
            )
            
        return main

@solara.component
def ModelInfo(index: int, model: str, task, is_last: bool = False):
    """Display LLM info.
    Used to label LLM response.
    """
    
    # do not show label while we are streaming the last message response. 
    if not is_last or not task.pending:
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
                ModelLabel(index, model, task, is_last)
                rv.Btn(
                    children=[
                        rv.Icon(
                            children=["mdi-creation"],
                        )
                    ],
                    icon=True,
                )

@solara.component
def ModelLabel(index: int, model: str, task, is_last: bool = False):
    """Display the model name."""
    # TODO REFACTOR AGAIN
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


@solara.component
def Page():
    # hide solara message at the bottom ("This website runs on solara")
    solara.Style(FILE_PATH.joinpath("style.css")) 
    solara.Title("Aithena")

    def user_send(message):
        """"Update the message history when user send a new message."""
        messages.value = [
            *messages.value,
            {"role": "user", "content": message},
        ]

    def call_llm():
        """Send history to the llm and update it with the response."""
        if user_message_count == 0:
            return
        response = current_llm.value.stream_chat(messages=messages.value)
        messages.value = [
            *messages.value,
            {"role": "assistant", "content": ""},
        ]
        for chunk in response:
            if chunk:
                add_chunk_to_ai_message(chunk.delta)

    def add_chunk_to_ai_message(chunk: str):
        """Add next chunk to current llm response.
        This is needed when we are using LLMs in stream mode.
        """
        messages.value = [
            *messages.value[:-1],
            {
                "role": "assistant",
                "content": messages.value[-1]["content"] + chunk,
            },
        ]

    # call the llm with the message history whenever the context has changed
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
        ChatOptions()

        with solara.lab.ChatBox():
            """Display message history."""
            for index, item in enumerate(messages.value):
                is_last = index == len(messages.value) - 1
                if item["role"] == "system": # do not display system prompt
                    continue
                if item["content"] == "": # do not display initial empty message content
                    continue
                with solara.Column(gap="0px"):
                    with solara.Div(style={"background-color": "rgba(0,0,0.3, 0.06)"}):
                        """Display a message.
                        NOTE ChatMessage work as a container, and has a children component.
                        For editable message, we pass on our component that will replace the 
                        default Markdown component that just display the message content.
                        """
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
                        """display the model name under the llm response."""
                        if current_llm.value.class_name == "azure_openai_llm":
                            ModelInfo(
                                index,
                                f"azure/{current_llm.value.engine}",
                                task,
                                is_last,
                            )
                        else:
                            ModelInfo(index, current_llm.value.model, task, is_last)

        """Anchor the chat input at the bottom of the screen."""
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
