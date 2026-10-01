# Note ingestion service

from src.rag.ingestion.chunker import Chunker
from src.rag.ingestion.embedder import embedder


class IngestionService:
    """Convert note content into chunks and embeddings."""

    def __init__(self):
        self.chunker = Chunker()

    def process_note(self, content: str) -> list[dict]:
        """Split note content and generate embeddings."""
        chunks = self.chunker.split_text(content)

        return [
            {
                "content": chunk,
                "chunk_index": index,
                "embedding": embedder.embed_text(chunk),
            }
            for index, chunk in enumerate(chunks)
        ]


ingestion_service = IngestionService()