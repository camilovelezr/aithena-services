import solara

from chatbot_dash.config import LLMS_AVAILABLE, PROMPT
import reacton.ipyvuetify as rv


@solara.component
def ChatOptions(llm_name, messages, edit_mode, reset_on_change):
    """Chat Options Component.
    
    We can currently:
    - select a specific llms depending on configured sources.
    - edit llms responses
    - reset history on model change.
    """

    def change_llm_name(*args):
        """Change the selected LLM."""
        llm_name.value = args[-1]
        if reset_on_change.value:
            messages.value = [{"role": "system", "content": PROMPT}]
            return
        return


    def change_reset_value(v):
        """Change the reset_on_change value."""
        reset_on_change.value = v


    def change_edit_mode_value(v):
        """Change the edit_mode value."""
        edit_mode.value = v

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
            label="Model", dense=True, items=LLMS_AVAILABLE, value=llm_name.value
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