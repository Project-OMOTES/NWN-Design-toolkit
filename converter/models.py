"""Data structures describing the tutorial content read from the workbook."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Link:
    text: str
    url: str


@dataclass
class Step:
    text: str
    mapeditor: Link | None = None
    tpg: Link | None = None


@dataclass
class Tutorial:
    title: str
    explanation: list[str] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)


@dataclass
class Section:
    name: str
    tutorials: list[Tutorial] = field(default_factory=list)
