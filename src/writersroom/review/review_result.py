from dataclasses import dataclass
from dataclasses import field

from writersroom.review.review_item import (
    ReviewItem,
)


@dataclass
class ReviewResult:
    """Results of a review."""

    items: list[
        ReviewItem
    ] = field(
        default_factory=list
    )

    @property
    def accepted_items(
        self,
    ) -> list[ReviewItem]:
        return [
            item
            for item in self.items
            if (
                item.decision.value
                != "reject"
            )
        ]

    @property
    def rejected_items(
        self,
    ) -> list[ReviewItem]:
        return [
            item
            for item in self.items
            if (
                item.decision.value
                == "reject"
            )
        ]