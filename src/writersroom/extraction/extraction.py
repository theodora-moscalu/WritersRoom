from dataclasses import dataclass
from dataclasses import field

from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)


@dataclass
class Extraction:
    """Represents one extraction run."""

    source_unit: SourceUnit

    agent: str

    claims: list[
        ExtractedClaim
    ] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )