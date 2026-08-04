from dataclasses import dataclass
from dataclasses import field

from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)


@dataclass
class ExtractionResult:
    """Claims extracted from a processed passage."""

    claims: list[
        ExtractedClaim
    ] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )