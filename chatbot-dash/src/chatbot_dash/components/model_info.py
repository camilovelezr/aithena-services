import solara
import reacton.ipyvuetify as rv


@solara.component
def ModelInfo(model_labels, index: int, model: str, task, is_last: bool = False):
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
                ModelLabel(model_labels, index, model, task, is_last)
                rv.Btn(
                    children=[
                        rv.Icon(
                            children=["mdi-creation"],
                        )
                    ],
                    icon=True,
                )

@solara.component
def ModelLabel(model_labels, index: int, model: str, task, is_last: bool = False):
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
