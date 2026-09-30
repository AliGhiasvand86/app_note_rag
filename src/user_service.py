# User management operations

from src.database import get_connection


def create_user(username):
    connection = get_connection()

    user_id = connection.execute(
        """
        INSERT INTO users (username)
        VALUES (%s)
        RETURNING id
        """,
        (username,)
    ).fetchone()[0]

    connection.commit()
    connection.close()

    return user_id


def get_user(user_id):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, created_at
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user