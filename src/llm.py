# LLM initialization

import os

from langchain_openai import ChatOpenAI

from src.config import (
    OPENROUTER_MODEL,
    TEMPERATURE,
    OPENROUTER_BASE_URL
)


def get_llm():

    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_base=OPENROUTER_BASE_URL,
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        temperature=TEMPERATURE
    )