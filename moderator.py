"""Copywriter agent: polishes tone, adds CTA, writes meta title/description."""

from crewai import Agent
from agents.llm import get_groq_llm


def build_copywriter_agent() -> Agent:
    return Agent(
        role="Copywriter",
        goal=(
            "Rewrite the draft for persuasive, on-brand tone, add a clear "
            "call-to-action, and produce an SEO meta title (<= 60 chars) "
            "and meta description (<= 155 chars)."
        ),
        backstory=(
            "You are a direct-response copywriter who specializes in "
            "e-commerce content. You sharpen weak sentences, tighten "
            "structure, and never let persuasive language drift into "
            "exaggerated or unverifiable claims."
        ),
        llm=get_groq_llm(temperature=0.7),
        verbose=True,
        allow_delegation=False,
    )
