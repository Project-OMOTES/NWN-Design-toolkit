"""Load the tutorial worksheet and return its relevant cells row by row."""

import re
from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils import column_index_from_string

from converter import config
from converter.models import Link

_URL_TEXT = re.compile(r"^(https?://|www\.)\S+$", re.IGNORECASE)


@dataclass(frozen=True)
class RawRow:
    row_number: int
    section: str | None
    title: str | None
    explanation: str | None
    step: str | None
    mapeditor: Link | None
    tpg: Link | None

    def is_empty(self) -> bool:
        return not any((self.section, self.title, self.explanation, self.step, self.mapeditor, self.tpg))


def _clean(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r\n", "\n").replace("\xa0", " ").strip()
    return text or None


def _link(cell: Cell) -> Link | None:
    """Return the external link of a cell: its hyperlink target, or its text when that is a URL."""
    text = _clean(cell.value)
    # Hyperlinks to a location within the workbook have no target and are ignored.
    target = _clean(cell.hyperlink.target) if cell.hyperlink is not None else None
    if target:
        return Link(text or target, target)
    if text and _URL_TEXT.match(text):
        url = text if text.lower().startswith("http") else f"https://{text}"
        return Link(text, url)
    return None


def read_rows(workbook_path: Path, sheet_name: str = config.DEFAULT_SHEET) -> list[RawRow]:
    """Return all non-empty data rows of the sheet, starting at config.FIRST_DATA_ROW."""
    # Not opened read-only: hyperlinks are only available in the normal mode.
    workbook = load_workbook(workbook_path, data_only=True)
    try:
        if sheet_name not in workbook.sheetnames:
            raise ValueError(f"Sheet '{sheet_name}' not found in {workbook_path}; available: {workbook.sheetnames}")
        sheet = workbook[sheet_name]

        def cell(row_number: int, column: str) -> Cell:
            return sheet.cell(row=row_number, column=column_index_from_string(column))

        rows: list[RawRow] = []
        for row_number in range(config.FIRST_DATA_ROW, sheet.max_row + 1):
            row = RawRow(
                row_number,
                section=_clean(cell(row_number, config.COLUMN_SECTION).value),
                title=_clean(cell(row_number, config.COLUMN_TITLE).value),
                explanation=_clean(cell(row_number, config.COLUMN_EXPLANATION).value),
                step=_clean(cell(row_number, config.COLUMN_STEP).value),
                mapeditor=_link(cell(row_number, config.COLUMN_MAPEDITOR)),
                tpg=_link(cell(row_number, config.COLUMN_TPG)),
            )
            if not row.is_empty():
                rows.append(row)
        return rows
    finally:
        workbook.close()
