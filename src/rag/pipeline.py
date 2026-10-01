# RAG retrieval pipeline

from src.rag.retrieval.context import build_context
from src.rag.retrieval.hybrid import hybrid_search
from src.rag.retrieval.reranker import reranker


class RAGPipeline:
    """Orchestrate hybrid retrieval, reranking, and context building."""

    def retrieve(
        self,
        query: str,
        user_id: int,
        top_k: int = 3,
        candidate_k: int = 10,
    ) -> str:
        """Retrieve and rerank relevant chunks and build the final context."""

        results = hybrid_search(
            query=query,
            user_id=user_id,
            top_k=candidate_k,
        )

        reranked_results = reranker.rerank(
            query=query,
            results=results,
            top_k=top_k,
        )

        return build_context(reranked_results)


rag_pipeline = RAGPipeline()