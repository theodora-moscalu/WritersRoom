from dataclasses import dataclass
from dataclasses import field

from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.review.review_decision import (
    ReviewDecision,
)


@dataclass
class ReviewItem:
    """Represents the review of one extracted claim."""

    claim: ExtractedClaim

    decision: ReviewDecision

    changes: dict[str, object] = field(
        default_factory=dict
    )

    comments: str = ""