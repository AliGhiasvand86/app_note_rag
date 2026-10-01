# RAG agent tool

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from src.rag.pipeline import rag_pipeline


@tool
def search_notes(query: str, config: RunnableConfig) -> str:
    """Retrieve relevant information from the authenticated user's notes."""

    user_id = config["configurable"]["user_id"]

    context = rag_pipeline.retrieve(
        query=query,
        user_id=user_id,
    )

    if not context:
        return "No relevant information was found in the user's notes."

    return context