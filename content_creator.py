"""
SEO Researcher agent.

Produces a content brief: working title, target keyword, search intent,
and an outline. In this starter, topic ideas come from prompting the LLM
with store-niche context (no paid keyword API required). Swap in a real
keyword tool later by adding a CrewAI `tool` to this agent.
"""

from crewai import Agent
from agents.llm import get_groq_llm
from config import config


def build_researcher_agent() -> Agent:
    return Agent(
        role="SEO Researcher",
        goal=(
            f"Identify a high-value, low-competition content topic for a "
            f"{config.STORE_NICHE}, and produce a clear content brief "
            f"(title, target keyword, search intent, and outline) that the "
            f"Content Creator can write from directly."
        ),
        backstory=(
            "You are a meticulous SEO strategist who has spent years "
            "researching search intent for niche e-commerce stores. You "
            "favor specific, answerable topics over broad ones, and you "
            "always state the searcher's underlying intent (informational, "
            "commercial, or transactional) explicitly."
        ),
        llm=get_groq_llm(temperature=0.6),
        verbose=True,
        allow_delegation=False,
    )
