# Summary management operations

from src.database import get_connection


def create_summary(note_id, summary_text):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO summaries (note_id, summary_text)
        VALUES (?, ?)
        """,
        (note_id, summary_text)
    )

    connection.commit()

    summary_id = cursor.lastrowid

    connection.close()

    return summary_id


def get_note_summaries(note_id):
    connection = get_connection()

    summaries = connection.execute(
        """
        SELECT id, summary_text, created_at
        FROM summaries
        WHERE note_id = ?
        ORDER BY created_at DESC
        """,
        (note_id,)
    ).fetchall()

    connection.close()

    return summaries


def get_latest_summary(note_id):
    connection = get_connection()

    summary = connection.execute(
        """
        SELECT id, summary_text, created_at
        FROM summaries
        WHERE note_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (note_id,)
    ).fetchone()

    connection.close()

    return summary


def delete_summary(summary_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM summaries
        WHERE id = ?
        """,
        (summary_id,)
    )

    connection.commit()

    connection.close()