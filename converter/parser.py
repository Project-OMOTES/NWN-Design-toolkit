"""Turn raw worksheet rows into sections, tutorials and steps.

The sheet is read top to bottom: a value in the section column starts a new
section, a value in the title column starts a new tutorial within the current
section and every value in the step column adds a step to the current tutorial.
"""

import logging

from converter.excel_reader import RawRow
from converter.models import Section, Step, Tutorial

logger = logging.getLogger(__name__)


def _paragraphs(text: str | None) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]


def parse_sections(rows: list[RawRow]) -> list[Section]:
    sections: list[Section] = []
    section: Section | None = None
    tutorial: Tutorial | None = None

    for row in rows:
        if row.section:
            section = Section(row.section)
            sections.append(section)
            tutorial = None

        if row.title:
            if section is None:
                logger.warning("Row %d: tutorial '%s' has no section; skipped", row.row_number, row.title)
                continue
            tutorial = Tutorial(row.title, explanation=_paragraphs(row.explanation))
            section.tutorials.append(tutorial)
        elif row.explanation:
            if tutorial is None:
                logger.warning("Row %d: explanation without tutorial; skipped", row.row_number)
            else:
                tutorial.explanation.extend(_paragraphs(row.explanation))

        if row.step:
            if tutorial is None:
                logger.warning("Row %d: step '%s' without tutorial; skipped", row.row_number, row.step)
            else:
                tutorial.steps.append(Step(row.step, mapeditor=row.mapeditor, tpg=row.tpg))

    return sections
