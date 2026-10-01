# Retrieved context builder


def build_context(results: list[dict]) -> str:
    """Build a context string from reranked retrieval results."""

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[Source {index}]\n"
            f"Title: {result['title']}\n"
            f"Content:\n{result['content']}"
        )

    return "\n\n".join(context_parts)