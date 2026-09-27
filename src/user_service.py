# User management operations

from src.database import get_connection


def create_user(username):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (username)
        VALUES (?)
        """,
        (username,)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user(user_id):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user