"""Chatbot multiple models."""

# pylint: disable=E1129, E1120, C0116, C0103
from pathlib import Path

import solara
import solara.lab
from component_utils import EditableMessage, ModelLabel, ModelRow

# import reacton.ipyvuetify as rv
from aithena_services.llms import Ollama  # type: ignore

FILE_PATH = Path(__file__).parent.absolute()

# PROMPT = """
# You are a helpful assistant named Aithena.
# Respond to users with witty, entertaining, and thoughtful answers.
# User wants short answers, maximum five sentences.
# If user asks info about yourself or your architecture,
# respond with info about your LLM model and its capabilities.
# Do not finish every sentence with a question.
# If you ask a question, always include a question mark.
# Do not introduce yourself to user if user does not ask for it.
# Never explain to user how your answers are.
# """
# PROMPT = """Pretend you are Albert Einstein and answer in two or three sentences each time."""

# MESSAGES = solara.reactive([{"role": "system", "content": PROMPT}])
MESSAGES: solara.Reactive[list] = solara.reactive([])


def add_chunk_to_ai_message(chunk: str):
    """Add chunk to assistant message."""
    MESSAGES.value = [
        *MESSAGES.value[:-1],
        {
            "role": "assistant",
            "content": MESSAGES.value[-1]["content"] + chunk,
        },
    ]


def change_llm_name(set_llm_name, reset_on_change, set_model_labels, *args):
    """Change the selected LLM."""
    set_llm_name(args[-1])
    if reset_on_change:
        MESSAGES.value = []
        set_model_labels({})
        return
    return


edit_index = solara.reactive(None)
current_edit_value = solara.reactive("")
# LLMS_AVAILABLE = requests.get("http://localhost:8000/chat/list", timeout=10).json()
# LLMS_AVAILABLE = [llm for llm in LLMS_AVAILABLE if not "embed" in llm]  # simple filter
LLMS_AVAILABLE = Ollama.list_models()


# Define the dictionary with reactive values
config = {
    "mirostat": solara.reactive(0),  # int (0, 1, 2)
    "mirostat_eta": solara.reactive(0.1),  # float (default 0.1)
    "mirostat_tau": solara.reactive(5.0),  # float (default 5.0)
    "num_ctx": solara.reactive(2048),  # int (default 2048)
    "repeat_last_n": solara.reactive(64),  # int (default 64)
    "repeat_penalty": solara.reactive(1.1),  # float (default 1.1)
    "temperature": solara.reactive(0.7),  # float (default 0.7)
    "seed": solara.reactive(42),  # int (default 0)
    "stop": solara.reactive(None),  # string
    "tfs_z": solara.reactive(1.0),  # float (default 1.0)
    "top_k": solara.reactive(40),  # int (default 40)
    "top_p": solara.reactive(0.9),  # float (default 0.9)
    "min_p": solara.reactive(0.05),  # float (default 0.0)
}


# The UI components
@solara.component
def ConfigCard():
    # Toggle switch to show or hide the card
    # Show the card if the toggle is active
    with solara.Column(gap="5px"):
        with solara.Card(
            title="LLM Configuration", elevation=2
        ):  # Add sliders and input fields based on the updated info
            solara.SliderInt(
                label="mirostat", value=config["mirostat"], min=0, max=2, step=1
            )
            solara.SliderFloat(
                label="mirostat_eta",
                value=config["mirostat_eta"],
                min=0.0,
                max=1.0,
                step=0.01,
            )
            solara.SliderFloat(
                label="mirostat_tau",
                value=config["mirostat_tau"],
                min=0.0,
                max=10.0,
                step=0.1,
            )
            solara.SliderInt(
                label="num_ctx", value=config["num_ctx"], min=0, max=10000, step=1
            )
            solara.SliderInt(
                label="repeat_last_n",
                value=config["repeat_last_n"],
                min=-1,
                max=config["num_ctx"].value,
                step=1,
            )
            solara.SliderFloat(
                label="repeat_penalty",
                value=config["repeat_penalty"],
                min=0.5,
                max=2.0,
                step=0.01,
            )
            solara.SliderFloat(
                label="temperature",
                value=config["temperature"],
                min=0.0,
                max=1.0,
                step=0.01,
            )
            solara.InputInt(
                label="seed",
                value=config["seed"],
            )
            solara.InputText(label="stop", value=config["stop"])
            solara.SliderFloat(
                label="tfs_z", value=config["tfs_z"], min=1.0, max=2.0, step=0.01
            )
            solara.SliderInt(
                label="top_k", value=config["top_k"], min=0, max=100, step=1
            )
            solara.SliderFloat(
                label="top_p", value=config["top_p"], min=0.0, max=1.0, step=0.01
            )
            solara.SliderFloat(
                label="min_p", value=config["min_p"], min=0.0, max=1.0, step=0.01
            )

        solara.Button(label="Reset Messages", on_click=lambda: MESSAGES.set([]))


@solara.component
def Page():
    solara.Style(FILE_PATH.joinpath("style.css"))
    solara.Title("Aithena")
    llm_options = LLMS_AVAILABLE

    llm_name, set_llm_name = solara.use_state("llama3.1")

    reset_on_change, set_reset_on_change = solara.use_state(False)

    edit_mode, set_edit_mode = solara.use_state(False)

    user_message_count = len([m for m in MESSAGES.value if m["role"] == "user"])

    is_menu_open, set_is_menu_open = solara.use_state(False)
    model_labels, set_model_labels = solara.use_state({})

    def user_send(message):
        print(f"Going to send user message: {message}")
        MESSAGES.value = [*MESSAGES.value, {"role": "user", "content": message}]
        print(f"Sent user message: {MESSAGES.value}")

    def call_llm():
        print(f"Calling LLM with {MESSAGES.value}")
        if user_message_count == 0:
            return
        ks = {k: v.value for k, v in config.items()}
        llm = Ollama(model=llm_name, **ks)
        print(llm)
        response = llm.stream_chat(MESSAGES.value)
        print(f"Sent messages to LLM: {MESSAGES.value}")
        msgs = [*MESSAGES.value, {"role": "assistant", "content": ""}]
        MESSAGES.value = msgs

        for chunk in response:
            if chunk:
                add_chunk_to_ai_message(chunk.delta)

    task = solara.lab.use_task(call_llm, dependencies=[user_message_count])  # type: ignore

    with solara.Sidebar():
        ConfigCard()

    with solara.Column(
        style={
            "width": "100%",
            "position": "relative",
            "height": "calc(100vh - 130px)",
            "padding-bottom": "15px",
            "overflow-y": "auto",
        },
    ):
        ModelRow(
            llm_options,
            llm_name,
            set_llm_name,
            set_model_labels,
            change_llm_name,
            reset_on_change,
            set_reset_on_change,
            MESSAGES.set,
            set_edit_mode,
        )
        with solara.lab.ChatBox():
            for index, item in enumerate(MESSAGES.value):
                is_last = index == len(MESSAGES.value) - 1
                if item["role"] == "system":
                    continue
                if item["role"] == "assistant" and item["content"] == "":
                    continue  # this avoids showing empty assistant messages
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
                            if edit_mode and item["role"] == "assistant":
                                EditableMessage(
                                    MESSAGES,
                                    item["content"],
                                    index,
                                    edit_index,
                                    current_edit_value,
                                )  # add 1 to index to account for prompt
                            else:
                                solara.Markdown(item["content"])
                    if item["role"] == "assistant":
                        ModelLabel(
                            index,
                            llm_name,
                            task,
                            model_labels,
                            set_model_labels,
                            is_menu_open,
                            set_is_menu_open,
                            is_last,
                        )
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
