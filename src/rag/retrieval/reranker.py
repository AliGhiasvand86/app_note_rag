# Reranking retrieved chunks

from FlagEmbedding import FlagReranker


MODEL_NAME = "BAAI/bge-reranker-v2-m3"


class Reranker:
    """Rerank retrieved chunks using a cross-encoder model."""

    def __init__(self):
        self.model = FlagReranker(
            MODEL_NAME,
            use_fp16=True,
        )

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 3,
    ) -> list[dict]:
        """Rerank retrieved chunks and return the most relevant results."""

        if not results:
            return []

        pairs = [
            [query, result["content"]]
            for result in results
        ]

        scores = self.model.compute_score(
            pairs,
            normalize=True,
        )

        if isinstance(scores, float):
            scores = [scores]

        reranked_results = []

        for result, score in zip(results, scores):
            reranked_result = result.copy()
            reranked_result["reranker_score"] = float(score)
            reranked_results.append(reranked_result)

        reranked_results.sort(
            key=lambda result: result["reranker_score"],
            reverse=True,
        )

        return reranked_results[:top_k]


reranker = Reranker()