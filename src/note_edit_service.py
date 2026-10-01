# Note editing and deletion with RAG synchronization

from src.note_service import delete_note, update_note
from src.rag.ingestion.repository import delete_chunks, save_chunks
from src.rag.ingestion.service import ingestion_service


def edit_note(
    user_id: int,
    note_id: int,
    title: str,
    content: str,
) -> bool:
    """Update a note and rebuild its RAG chunks."""

    updated = update_note(
        user_id=user_id,
        note_id=note_id,
        title=title,
        content=content,
    )

    if not updated:
        return False

    delete_chunks(note_id)

    chunks = ingestion_service.process_note(content)

    save_chunks(
        note_id=note_id,
        chunks=chunks,
    )

    return True


def remove_note(
    user_id: int,
    note_id: int,
) -> bool:
    """Delete a note and all of its RAG chunks."""

    deleted = delete_note(
        user_id=user_id,
        note_id=note_id,
    )

    if not deleted:
        return False

    delete_chunks(note_id)

    return True