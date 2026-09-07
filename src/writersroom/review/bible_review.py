from dataclasses import dataclass
from dataclasses import field

from writersroom.review.review_decision import (
    ReviewDecision,
)


@dataclass
class BibleReviewItem:
    """One entity proposed from a bible, matched against the current project."""

    kind: str  # character | relationship | season | episode | location | note
    proposed: object
    existing: object | None = None
    decision: ReviewDecision = ReviewDecision.ACCEPT

    @property
    def is_update(self) -> bool:
        return self.existing is not None

    def label(self) -> str:
        if self.kind == "relationship":
            name = (
                f"{self.proposed.source} "
                f"--{self.proposed.relationship.value}--> "
                f"{self.proposed.target}"
            )
        elif self.kind == "season":
            name = str(self.proposed)
        else:
            name = getattr(
                self.proposed,
                "name",
                "",
            ) or getattr(
                self.proposed,
                "title",
                "",
            )

        tag = "update" if self.is_update else "new"

        return f"[{tag}] {self.kind}: {name}"


@dataclass
class BibleReview:
    """The full set of proposed bible entities awaiting the writer's decision."""

    items: list[BibleReviewItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def accepted_items(self) -> list[BibleReviewItem]:
        return [
            item
            for item in self.items
            if item.decision != ReviewDecision.REJECT
        ]
