# Keyword retrieval with PostgreSQL full-text search

from src.database import get_connection


def keyword_search(
    query: str,
    user_id: int,
    top_k: int = 5,
) -> list[dict]:
    """Retrieve chunks using PostgreSQL full-text search."""

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            chunks.id,
            chunks.note_id,
            notes.title,
            chunks.content,
            chunks.chunk_index,
            ts_rank(
                to_tsvector('simple', chunks.content),
                plainto_tsquery('simple', %s)
            ) AS score
        FROM chunks
        JOIN notes
            ON chunks.note_id = notes.id
        WHERE
            notes.user_id = %s
            AND to_tsvector('simple', chunks.content)
                @@ plainto_tsquery('simple', %s)
        ORDER BY score DESC
        LIMIT %s
        """,
        (
            query,
            user_id,
            query,
            top_k,
        ),
    ).fetchall()

    connection.close()

    return [
        {
            "chunk_id": row[0],
            "note_id": row[1],
            "title": row[2],
            "content": row[3],
            "chunk_index": row[4],
            "keyword_score": row[5],
        }
        for row in rows
    ]