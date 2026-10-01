# Semantic retrieval with pgvector

from src.database import get_connection
from src.rag.ingestion.embedder import embedder


def semantic_search(
    query: str,
    user_id: int,
    top_k: int = 5,
) -> list[dict]:
    """Retrieve the most semantically similar chunks for a user's query."""

    query_embedding = embedder.embed_text(query)

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            chunks.id,
            chunks.note_id,
            notes.title,
            chunks.content,
            chunks.chunk_index,
            1 - (chunks.embedding <=> %s::vector) AS similarity
        FROM chunks
        JOIN notes
            ON chunks.note_id = notes.id
        WHERE notes.user_id = %s
        ORDER BY chunks.embedding <=> %s::vector
        LIMIT %s
        """,
        (
            query_embedding,
            user_id,
            query_embedding,
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
            "semantic_score": row[5],
        }
        for row in rows
    ]