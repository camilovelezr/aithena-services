"""Chatbot multiple models."""

# pylint: disable=E1129, E1120, C0116, C0103
import json
from copy import copy
from pathlib import Path

import reacton.ipyvuetify as rv
import solara
import solara.lab


from .components.chat_options import ChatOptions
from .config import FILE_PATH, LLM_DICT, PROMPT


"""history will be erased on model change."""
reset_on_change: solara.Reactive[bool] = solara.Reactive(False)
"""Make all assistant reponse editable."""
# TODO not sure how useful it is, as the previous conversation may
# become inconsitent.
edit_mode: solara.Reactive[bool] = solara.Reactive(False)

# global state : we kept track of message history
# we initialize history with the system prompt
messages: solara.Reactive[list[dict]] = solara.reactive(
    ([{"role": "system", "content": PROMPT}])
)
edit_index = solara.reactive(None)
current_edit_value = solara.reactive("")
model_labels: solara.Reactive[dict[int, str]] = solara.reactive({})
is_menu_open = solara.reactive(False)

"""LLM currently selected."""
llm_name: solara.Reactive[str] = (
    solara.reactive("llama3.1")
    if "llama3.1" in LLM_DICT
    else solara.reactive(list(LLM_DICT.keys())[0])
)
# LLM selected 
current_llm: solara.Reactive[LLM] = solara.reactive(  # type: ignore
    LLM_DICT[llm_name.value]
)
user_message_count = len([m for m in messages.value if m["role"] == "user"])


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
        ChatOptions(llm_name, messages, edit_mode, reset_on_change)

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
                            if edit_mode.value and item["role"] == "assistant":
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
