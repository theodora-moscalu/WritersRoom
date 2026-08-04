from writersroom.extraction.extraction_result import (
    ExtractionResult,
)
from writersroom.review.review_decision import (
    ReviewDecision,
)
from writersroom.review.review_item import (
    ReviewItem,
)
from writersroom.review.review_result import (
    ReviewResult,
)


class ReviewService:
    """Coordinates claim review."""

    def review(
        self,
        extraction: ExtractionResult,
    ) -> ReviewResult:
        """Review extracted claims."""

        items = []

        for claim in extraction.claims:

            items.append(
                ReviewItem(
                    claim=claim,
                    decision=(
                        ReviewDecision.ACCEPT
                    ),
                )
            )

        return ReviewResult(
            items=items,
        )