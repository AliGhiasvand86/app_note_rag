# Note management operations

from src.database import get_connection


def create_note(user_id, title, content):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (user_id, title, content)
        VALUES (?, ?, ?)
        """,
        (user_id, title, content)
    )

    connection.commit()

    note_id = cursor.lastrowid

    connection.close()

    return note_id


def get_user_notes(user_id):
    connection = get_connection()

    notes = connection.execute(
        """
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return notes


def get_note(note_id):
    connection = get_connection()

    note = connection.execute(
        """
        SELECT id, user_id, title, content, created_at, updated_at
        FROM notes
        WHERE id = ?
        """,
        (note_id,)
    ).fetchone()

    connection.close()

    return note


def update_note(note_id, title, content):
    connection = get_connection()

    connection.execute(
        """
        UPDATE notes
        SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (title, content, note_id)
    )

    connection.commit()

    connection.close()


def delete_note(note_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM notes
        WHERE id = ?
        """,
        (note_id,)
    )

    connection.commit()

    connection.close()