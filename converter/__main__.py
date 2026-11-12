"""Command line entry point: python -m converter [workbook] [--sheet NAME]."""

import argparse
import logging
from pathlib import Path

from converter import config
from converter.excel_reader import read_rows
from converter.models import Section
from converter.parser import parse_sections
from converter.rst import design_pages, step_by_step
from converter.writer import write_pages

logger = logging.getLogger("converter")


def build_pages(sections: list[Section]) -> dict[Path, str]:
    pages: dict[Path, str] = {}
    section_pages = []
    for section in sections:
        if not config.is_known_section(section.name):
            logger.warning(
                "Section '%s' is not in config.SECTION_PAGES; add it there and to design_with_the_toolkit.rst",
                section.name,
            )
        section_page = config.pages_for_section(section.name)
        section_pages.append(section_page)
        step_by_step_dir = config.STEP_BY_STEP_DIR / section_page.step_by_step_folder
        page_names = step_by_step.tutorial_page_names(section, section_page)

        for tutorial, page_name in zip(section.tutorials, page_names, strict=True):
            pages[step_by_step_dir / f"{page_name}.rst"] = step_by_step.render_tutorial_page(tutorial)
        pages[config.STEP_BY_STEP_DIR / f"{section_page.step_by_step_index}.rst"] = (
            step_by_step.render_section_index(section, page_names)
        )

        step_by_step_docs = [step_by_step.tutorial_doc(section_page, name) for name in page_names]
        pages[config.DESIGN_DIR / f"{section_page.design_page}.rst"] = design_pages.render_section_page(
            section, step_by_step_docs
        )
    pages[config.STEP_BY_STEP_DIR / "step_by_step.rst"] = step_by_step.render_landing_page(section_pages)
    return pages


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate the tutorial RST pages from the Excel table of contents.")
    parser.add_argument("workbook", nargs="?", type=Path, default=config.DEFAULT_WORKBOOK, help="Excel workbook")
    parser.add_argument("--sheet", default=config.DEFAULT_SHEET, help="worksheet with the tutorials")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    rows = read_rows(args.workbook, args.sheet)
    sections = parse_sections(rows)
    written = write_pages(build_pages(sections))

    for path in written:
        logger.info("Written %s", path.relative_to(config.REPO_ROOT))


if __name__ == "__main__":
    main()
