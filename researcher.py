"""Publisher agent: not an LLM call -- a thin wrapper that pushes the final
copy to WordPress via the REST API. Kept separate from agent reasoning so
publishing is deterministic and auditable."""

from crewai import Agent
from agents.llm import get_groq_llm


def build_publisher_agent() -> Agent:
    """
    This agent exists mainly so CrewAI's task/crew structure stays uniform.
    The actual HTTP call to WordPress happens in wordpress_client.py,
    invoked from crew.py after the Editor's task completes -- not via LLM
    tool-calling -- so a network failure can be retried deterministically
    without re-running the whole content pipeline.
    """
    return Agent(
        role="Publisher",
        goal=(
            "Prepare the final copy and metadata exactly as received from "
            "the Editor for publishing, with no further content changes."
        ),
        backstory=(
            "You are a meticulous operations assistant. You never alter "
            "wording -- you only format content for the WordPress REST API "
            "(title, body HTML, categories, tags, status)."
        ),
        llm=get_groq_llm(temperature=0.0),
        verbose=True,
        allow_delegation=False,
    )
