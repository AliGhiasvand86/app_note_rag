# Text chunking utilities

from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:
    """Split text into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_text(self, text: str) -> list[str]:
        """Split text into chunks."""
        return self.splitter.split_text(text)