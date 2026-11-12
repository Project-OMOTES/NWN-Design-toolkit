"""Save rendered pages to disk."""

from pathlib import Path


def write_pages(pages: dict[Path, str]) -> list[Path]:
    """Write every page, creating parent directories and overwriting existing files."""
    written = []
    for path, content in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        written.append(path)
    return written
