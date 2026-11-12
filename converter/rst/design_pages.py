"""Topic pages of the "Design with the Toolkit" tutorial section."""

from converter.models import Section, Tutorial
from converter.rst import helpers


def _tutorial_item(tutorial: Tutorial, step_by_step_doc: str) -> list[str]:
    lines = [f"**{helpers.escape(tutorial.title)}**", ""]
    for paragraph in tutorial.explanation:
        lines += [helpers.escape(paragraph), ""]
    lines.append(f"See :doc:`step by step <{step_by_step_doc}>`.")
    return helpers.bullet_item(lines)


def render_section_page(section: Section, step_by_step_docs: list[str]) -> str:
    """Render a topic page; step_by_step_docs holds the step-by-step document of every tutorial."""
    lines = helpers.heading(section.name, "=")

    if not section.tutorials:
        lines += ["Content for this topic will be added.", ""]

    for tutorial, step_by_step_doc in zip(section.tutorials, step_by_step_docs, strict=True):
        lines += _tutorial_item(tutorial, step_by_step_doc)

    return helpers.page(lines)
