# Note summarization module

from src.llm import get_llm


SUMMARY_PROMPT = """
You are an expert note summarization assistant.

Your task is to summarize the user's note.

Rules:
- Preserve the main ideas and important details.
- Remove unnecessary repetition.
- Do not add information that is not present in the note.
- Make the summary clear and structured.
- Use bullet points when the content contains multiple ideas.
- Keep technical terms unchanged.

Note:

{note_content}

Summary:
"""


def generate_summary(note_content: str) -> str:
    """
    Generate a summary for a given note content.
    """

    llm = get_llm()

    prompt = SUMMARY_PROMPT.format(
        note_content=note_content
    )

    response = llm.invoke(prompt)

    return response.content