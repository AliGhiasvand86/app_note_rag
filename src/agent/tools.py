# Agent tools

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from src.note_service import (
    create_note,
    get_note_by_title,
    delete_note,
)
from src.summary_service import create_summary
from src.summarizer import generate_summary


def _get_user_id(config: RunnableConfig) -> int:
    return config["configurable"]["user_id"]


@tool
def create_note_tool(title: str, content: str, config: RunnableConfig) -> str:
    """Create a new note for the authenticated user with a title and content."""

    user_id = _get_user_id(config)

    create_note(
        user_id=user_id,
        title=title,
        content=content,
    )

    return f"Note '{title}' created successfully."


@tool
def summarize_note_tool(title: str, config: RunnableConfig) -> str:
    """Generate and save an AI summary for a note belonging to the authenticated user by its title."""

    user_id = _get_user_id(config)

    note = get_note_by_title(
        user_id=user_id,
        title=title,
    )

    if note is None:
        return f"Note '{title}' was not found."

    note_id = note[0]
    content = note[3]

    summary = generate_summary(content)

    create_summary(
        note_id=note_id,
        summary_text=summary,
    )

    return summary


@tool
def delete_note_tool(title: str, config: RunnableConfig) -> str:
    """Delete a note belonging to the authenticated user by its title."""

    user_id = _get_user_id(config)

    note = get_note_by_title(
        user_id=user_id,
        title=title,
    )

    if note is None:
        return f"Note '{title}' was not found."

    note_id = note[0]

    delete_note(note_id)

    return f"Note '{title}' deleted successfully."


tools = [
    create_note_tool,
    summarize_note_tool,
    delete_note_tool,
]