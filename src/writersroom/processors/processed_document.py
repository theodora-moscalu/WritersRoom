from dataclasses import dataclass
from dataclasses import field

from writersroom.processors.source_unit import (
    SourceUnit,
)


@dataclass
class ProcessedDocument:
    """A processed document ready for knowledge extraction."""

    source_units: list[
        SourceUnit
    ]

    metadata: dict[str, str] = field(
        default_factory=dict
    )