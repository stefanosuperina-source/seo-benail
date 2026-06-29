"""
Shared CrewAI LLM wrapper pointing at Groq via LiteLLM.

CrewAI agents accept a `litellm`-style model string directly, so swapping
providers later (e.g. to OpenAI or Anthropic) is just changing this one
string + the matching API key env var.
"""

from crewai import LLM
from config import config


def get_groq_llm(temperature: float = 0.7) -> LLM:
    return LLM(
        model=config.GROQ_MODEL,          # e.g. "groq/llama-3.3-70b-versatile"
        api_key=config.GROQ_API_KEY,
        temperature=temperature,
    )
