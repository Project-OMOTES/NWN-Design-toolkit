"""Pages of the "Step by step" tutorial section.

Every section gets a folder with an index page, and every tutorial in it a
page of its own with a table of its steps.
"""

import re

from converter import config
from converter.config import SectionPages
from converter.models import Link, Section, Step, Tutorial
from converter.rst import helpers

TABLE_HEADER = ["Step", "ESDL Mapeditor", "TPG front end"]
TABLE_WIDTHS = [60, 20, 20]

_LETTER_PREFIX = re.compile(r"^([A-Za-z])[.)]\s")


def tutorial_page_names(section: Section, pages: SectionPages) -> list[str]:
    """Return the page name (without extension) of every tutorial in the section, in order.

    The suffix is the letter prefix of the title ("A. ..." -> _step_a), or the
    position (a, b, ...) when the title has none or the letter is already used.
    """
    names: list[str] = []
    for index, tutorial in enumerate(section.tutorials):
        match = _LETTER_PREFIX.match(tutorial.title)
        suffix = match.group(1).lower() if match else _position_suffix(index)
        name = f"{pages.step_by_step_folder}_step_{suffix}"
        if name in names:
            name = f"{pages.step_by_step_folder}_step_{_position_suffix(index)}"
        while name in names:
            name += "_"
        names.append(name)
    return names


def _position_suffix(index: int) -> str:
    """0 -> a, 25 -> z, 26 -> aa, ..."""
    suffix = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        suffix = chr(ord("a") + remainder) + suffix
    return suffix


def tutorial_doc(pages: SectionPages, page_name: str) -> str:
    """Absolute Sphinx document name of a tutorial page, for :doc: references."""
    step_by_step_doc = config.STEP_BY_STEP_DIR.relative_to(config.SOURCE_DIR).as_posix()
    return f"/{step_by_step_doc}/{pages.step_by_step_folder}/{page_name}"


def _practical_use_cell(link: Link | None) -> list[str]:
    """The placeholder picture linking to the cell's link; empty when there is no link."""
    if link is None:
        return []
    # Line breaks would end the :alt: option of the image directive.
    alt = " ".join(link.text.split())
    return helpers.image(config.PLACEHOLDER_IMAGE, alt, config.PLACEHOLDER_IMAGE_WIDTH, target=link.url)


def _step_row(step: Step) -> list[list[str]]:
    return [
        [helpers.escape(step.text)],
        _practical_use_cell(step.mapeditor),
        _practical_use_cell(step.tpg),
    ]


def render_tutorial_page(tutorial: Tutorial) -> str:
    lines = helpers.heading(tutorial.title, "=")
    if tutorial.steps:
        lines += helpers.list_table(TABLE_HEADER, [_step_row(step) for step in tutorial.steps], TABLE_WIDTHS)
    else:
        lines += ["The steps for this tutorial will be added.", ""]
    return helpers.page(lines)


def render_section_index(section: Section, page_names: list[str]) -> str:
    lines = helpers.heading(section.name, "=")
    if page_names:
        lines += [".. toctree::", "   :maxdepth: 1", "", *[f"   {name}" for name in page_names]]
    else:
        lines += ["Content for this topic will be added.", ""]
    return helpers.page(lines)


def render_landing_page(section_pages: list[SectionPages]) -> str:
    lines = [
        *helpers.heading("Step by step", "="),
        "Design questions for the Toolkit => subsequent actions to come to answers.",
        "",
        "Each topic of :doc:`Design with the Toolkit </tutorials/design_with_the_toolkit/design_with_the_toolkit>`",
        "is worked out here step by step, together with where to perform each step in the Toolkit.",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "",
        *[f"   {pages.step_by_step_index}" for pages in section_pages],
    ]
    return helpers.page(lines)
