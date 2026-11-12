"""Paths, workbook layout and page naming used by the converter."""

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"
TUTORIALS_DIR = SOURCE_DIR / "tutorials"
DESIGN_DIR = TUTORIALS_DIR / "design_with_the_toolkit"
STEP_BY_STEP_DIR = TUTORIALS_DIR / "step_by_step"

DEFAULT_WORKBOOK = REPO_ROOT / "Table of Contents Tutorials DTK.xlsx"
DEFAULT_SHEET = "Tutorials"

# Workbook layout of the Tutorials sheet.
FIRST_DATA_ROW = 5
COLUMN_SECTION = "B"
COLUMN_TITLE = "C"
COLUMN_EXPLANATION = "D"
COLUMN_STEP = "E"
COLUMN_MAPEDITOR = "F"
COLUMN_TPG = "G"

# Placeholder shown in the practical use columns; the path is relative to the Sphinx source dir.
PLACEHOLDER_IMAGE = "/images/esdl.svg"
PLACEHOLDER_IMAGE_WIDTH = "60px"


@dataclass(frozen=True)
class SectionPages:
    design_page: str
    """Document path relative to DESIGN_DIR, without extension."""
    step_by_step_folder: str
    """Folder within STEP_BY_STEP_DIR holding the asset index page and one page per tutorial."""

    @property
    def step_by_step_index(self) -> str:
        """Document path of the asset index page, relative to STEP_BY_STEP_DIR."""
        return f"{self.step_by_step_folder}/{self.step_by_step_folder}"


# Keys are the lower-cased section names of column B; design pages match the
# toctree in design_with_the_toolkit.rst.
SECTION_PAGES: dict[str, SectionPages] = {
    "demand": SectionPages("Demand/demand", "demand"),
    "production": SectionPages("Production/production", "production"),
    "storage": SectionPages("Storage/storage", "storage"),
    "heat pumps": SectionPages("Heat pumps/heat_pump", "heat_pumps"),
    "thermal plots (warmtekavels)": SectionPages("Thermal plots/thermal_plots", "thermal_plots"),
    "transport": SectionPages("Transport/transport", "transport"),
    "other": SectionPages("Other/other", "other"),
}


def is_known_section(name: str) -> bool:
    return name.strip().lower() in SECTION_PAGES


def pages_for_section(name: str) -> SectionPages:
    """Return the page paths of a section; unknown sections get paths derived from their name."""
    known = SECTION_PAGES.get(name.strip().lower())
    if known:
        return known
    slug = re.sub(r"[^0-9a-z]+", "_", name.strip().lower()).strip("_") or "section"
    return SectionPages(f"{slug}/{slug}", slug)
