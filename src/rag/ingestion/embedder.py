# Embedding model management

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"


class Embedder:
    """Generate dense embeddings using the BGE-M3 model."""

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()


embedder = Embedder()