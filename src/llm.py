# LLM initialization

import os

from langchain_openai import ChatOpenAI

from src.config import GROQ_MODEL, TEMPERATURE


def get_llm():
    return ChatOpenAI(
        model=GROQ_MODEL,
        temperature=TEMPERATURE,
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )