# Metadata filtering for retrieval results

def filter_results(
    results: list[dict],
    note_id: int | None = None,
    title: str | None = None,
) -> list[dict]:
    """Filter retrieval results using optional note metadata."""

    filtered_results = results

    if note_id is not None:
        filtered_results = [
            result
            for result in filtered_results
            if result["note_id"] == note_id
        ]

    if title is not None:
        normalized_title = title.strip().lower()

        filtered_results = [
            result
            for result in filtered_results
            if result["title"].strip().lower() == normalized_title
        ]

    return filtered_results