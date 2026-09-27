# Note AI workflow operations

from src.note_service import get_note
from src.summarizer import generate_summary
from src.summary_service import create_summary


def summarize_note(note_id: int):
    note = get_note(note_id)

    if note is None:
        raise ValueError("Note not found")

    content = note[3]

    summary_text = generate_summary(content)

    summary_id = create_summary(
        note_id,
        summary_text
    )

    return {
        "summary_id": summary_id,
        "summary": summary_text
    }