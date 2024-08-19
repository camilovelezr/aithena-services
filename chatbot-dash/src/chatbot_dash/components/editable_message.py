from copy import copy
import solara


@solara.component
def EditableMessage(messages, message, index, edit_index, current_edit_value):
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