"""
Main entry point. Wires the six agents into a CrewAI sequential pipeline:

    Researcher -> Content Creator -> Copywriter -> Moderator -> Editor
    -> (deterministic) WordPress publish step

The Moderator's verdict gates publishing: if it returns FLAGGED, the run
stops and prints the issues instead of publishing, so nothing risky goes
live unattended.

Run:
    python crew.py
"""

import re
import sys
from pathlib import Path

from crewai import Crew, Task, Process

from agents.researcher import build_researcher_agent
from agents.content_creator import build_content_creator_agent
from agents.copywriter import build_copywriter_agent
from agents.moderator import build_moderator_agent
from agents.editor import build_editor_agent
from wordpress_client import WordPressClient
from config import config


def build_tasks():
    researcher = build_researcher_agent()
    creator = build_content_creator_agent()
    copywriter = build_copywriter_agent()
    moderator = build_moderator_agent()
    editor = build_editor_agent()

    brief_task = Task(
        description=(
            f"Research a content topic for a {config.STORE_NICHE}. "
            "Output a content brief with these exact labeled fields:\n"
            "TITLE: ...\nTARGET_KEYWORD: ...\nINTENT: ...\nOUTLINE:\n- ...\n- ..."
        ),
        expected_output="A labeled content brief as specified above.",
        agent=researcher,
    )

    draft_task = Task(
        description=(
            "Using the content brief above, write a complete first draft "
            "(600-900 words) in HTML paragraph/heading tags (<h2>, <p>, "
            "<ul>/<li>), following the outline closely."
        ),
        expected_output="A complete HTML draft of the blog post.",
        agent=creator,
        context=[brief_task],
    )

    polish_task = Task(
        description=(
            "Rewrite the draft above for persuasive, on-brand tone and add "
            "a clear call-to-action near the end. Then output exactly in "
            "this format:\nMETA_TITLE: ...\nMETA_DESCRIPTION: ...\n"
            "CONTENT_HTML:\n<the full polished HTML>"
        ),
        expected_output=(
            "META_TITLE, META_DESCRIPTION, and CONTENT_HTML fields as specified."
        ),
        agent=copywriter,
        context=[draft_task],
    )

    moderation_task = Task(
        description=(
            "Review the CONTENT_HTML above against the moderation "
            "guidelines. Output exactly in this format:\n"
            "VERDICT: PASS or FLAGGED\nISSUES:\n- (none, or list each "
            "issue with the exact quoted phrase)"
        ),
        expected_output="VERDICT and ISSUES fields as specified.",
        agent=moderator,
        context=[polish_task],
    )

    edit_task = Task(
        description=(
            "If VERDICT is FLAGGED, do not proceed -- instead output "
            "'BLOCKED: see moderation issues' and stop. If VERDICT is "
            "PASS, perform a final grammar/clarity pass on CONTENT_HTML, "
            "suggest 2-3 internal link anchor texts as a comment, and "
            "output the final result in this exact format:\n"
            "STATUS: READY or BLOCKED\nMETA_TITLE: ...\n"
            "META_DESCRIPTION: ...\nCATEGORY: ...\nTAGS: tag1, tag2, tag3\n"
            "CONTENT_HTML:\n<final HTML>"
        ),
        expected_output="STATUS plus full publish-ready fields as specified.",
        agent=editor,
        context=[polish_task, moderation_task],
    )

    return [brief_task, draft_task, polish_task, moderation_task, edit_task]


def parse_editor_output(raw: str) -> dict:
    """Parses the Editor's final labeled-field output into a dict."""
    fields = {}
    status_match = re.search(r"STATUS:\s*(\w+)", raw)
    fields["status"] = status_match.group(1) if status_match else "BLOCKED"

    for key in ["META_TITLE", "META_DESCRIPTION", "CATEGORY", "TAGS"]:
        m = re.search(rf"{key}:\s*(.+)", raw)
        fields[key.lower()] = m.group(1).strip() if m else ""

    content_match = re.search(r"CONTENT_HTML:\s*(.+)", raw, re.DOTALL)
    fields["content_html"] = content_match.group(1).strip() if content_match else ""
    return fields


def main():
    tasks = build_tasks()
    crew = Crew(
        agents=[t.agent for t in tasks],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    raw_output = str(result)

    Path(config.OUTPUT_DIR).mkdir(exist_ok=True)
    out_file = Path(config.OUTPUT_DIR) / "last_run.txt"
    out_file.write_text(raw_output, encoding="utf-8")
    print(f"\nFull pipeline output saved to {out_file}")

    parsed = parse_editor_output(raw_output)

    if parsed["status"] != "READY":
        print("\nBLOCKED: moderation flagged this draft. Not publishing.")
        print("Review", out_file, "for the moderator's specific issues.")
        sys.exit(1)

    title = parsed["meta_title"] or "Untitled post"
    tags = [t.strip() for t in parsed["tags"].split(",") if t.strip()]
    category = [parsed["category"]] if parsed["category"] else []

    print(f"\nPublishing '{title}' to WordPress as status={config.PUBLISH_STATUS}...")
    wp = WordPressClient()
    post = wp.create_post(
        title=title,
        content_html=parsed["content_html"],
        category_names=category,
        tag_names=tags,
        meta_description=parsed["meta_description"],
    )
    print(f"Done. Post ID {post.get('id')} -- status: {post.get('status')}")
    print(f"Edit it at: {config.WP_URL}/wp-admin/post.php?post={post.get('id')}&action=edit")


if __name__ == "__main__":
    main()
