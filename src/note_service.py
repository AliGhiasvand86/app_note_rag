# Note management operations

from src.database import get_connection


def create_note(user_id: int, title: str, content: str) -> int:
    connection = get_connection()

    note_id = connection.execute(
        """
        INSERT INTO notes (user_id, title, content)
        VALUES (%s, %s, %s)
        RETURNING id
        """, 
        (user_id, title, content)
    ).fetchone()[0]

    connection.commit()
    connection.close()

    return note_id


def get_user_notes(user_id: int) -> list[tuple]:
    connection = get_connection()

    notes = connection.execute(
        """
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE user_id = %s
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return notes


def update_note(
    user_id: int,
    note_id: int,
    title: str,
    content: str,
) -> bool:
    connection = get_connection()

    result = connection.execute(
        """
        UPDATE notes
        SET title = %s,
            content = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
          AND user_id = %s
        """,
        (title, content, note_id, user_id),
    )

    connection.commit()
    connection.close()

    return result.rowcount > 0


def delete_note(
    user_id: int,
    note_id: int,
) -> bool:
    connection = get_connection()

    result = connection.execute(
        """
        DELETE FROM notes
        WHERE id = %s
          AND user_id = %s
        """,
        (note_id, user_id),
    )

    connection.commit()
    connection.close()

    return result.rowcount > 0

def get_note_by_title(user_id: int, title: str) -> tuple | None:
    connection = get_connection()

    note = connection.execute(
        """
        SELECT id, user_id, title, content, created_at, updated_at
        FROM notes
        WHERE user_id = %s AND title = %s
        """,
        (user_id, title),
    ).fetchone()

    connection.close()

    return note