# Chunk persistence operations

from src.database import get_connection


def delete_chunks(note_id: int) -> None:
    """Delete all chunks belonging to a note."""

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM chunks
        WHERE note_id = %s
        """,
        (note_id,),
    )

    connection.commit()
    connection.close()


def save_chunks(note_id: int, chunks: list[dict]) -> None:
    """Save note chunks and their embeddings to PostgreSQL."""

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO chunks (
                note_id,
                content,
                chunk_index,
                embedding
            )
            VALUES (%s, %s, %s, %s)
            """,
            [
                (
                    note_id,
                    chunk["content"],
                    chunk["chunk_index"],
                    chunk["embedding"],
                )
                for chunk in chunks
            ],
        )

    connection.commit()
    connection.close()