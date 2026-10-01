# Hybrid retrieval with reciprocal rank fusion

from src.rag.retrieval.keyword import keyword_search
from src.rag.retrieval.semantic import semantic_search


def hybrid_search(
    query: str,
    user_id: int,
    top_k: int = 5,
    candidate_k: int = 10,
    rrf_k: int = 60,
) -> list[dict]:
    """Combine semantic and keyword retrieval using reciprocal rank fusion."""

    semantic_results = semantic_search(
        query=query,
        user_id=user_id,
        top_k=candidate_k,
    )

    keyword_results = keyword_search(
        query=query,
        user_id=user_id,
        top_k=candidate_k,
    )

    fused_results = {}

    for rank, result in enumerate(semantic_results, start=1):
        chunk_id = result["chunk_id"]

        fused_results.setdefault(
            chunk_id,
            {
                "chunk_id": chunk_id,
                "note_id": result["note_id"],
                "title": result["title"],
                "content": result["content"],
                "chunk_index": result["chunk_index"],
                "semantic_score": 0.0,
                "keyword_score": 0.0,
                "rrf_score": 0.0,
            },
        )

        fused_results[chunk_id]["semantic_score"] = result["semantic_score"]
        fused_results[chunk_id]["rrf_score"] += 1 / (rrf_k + rank)

    for rank, result in enumerate(keyword_results, start=1):
        chunk_id = result["chunk_id"]

        fused_results.setdefault(
            chunk_id,
            {
                "chunk_id": chunk_id,
                "note_id": result["note_id"],
                "title": result["title"],
                "content": result["content"],
                "chunk_index": result["chunk_index"],
                "semantic_score": 0.0,
                "keyword_score": 0.0,
                "rrf_score": 0.0,
            },
        )

        fused_results[chunk_id]["keyword_score"] = result["keyword_score"]
        fused_results[chunk_id]["rrf_score"] += 1 / (rrf_k + rank)

    results = sorted(
        fused_results.values(),
        key=lambda result: result["rrf_score"],
        reverse=True,
    )

    return results[:top_k]