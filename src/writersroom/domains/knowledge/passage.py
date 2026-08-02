from writersroom.domains.knowledge.claim import (
    Claim,
)


class Passage:
    """Represents a contiguous passage within a document."""

    def __init__(
        self,
        identity: str,
        document_id: str,
        title: str = "",
        text: str = "",
        claims: list[Claim] | None = None,
    ):
        self.identity = identity
        self.document_id = document_id
        self.title = title
        self.text = text
        self.claims = claims or []

    def to_dict(self):
        """Convert the passage to a dictionary."""

        return {
            "identity": self.identity,
            "document_id": self.document_id,
            "title": self.title,
            "text": self.text,
            "claims": [
                claim.to_dict()
                for claim in self.claims
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Passage from a dictionary."""

        return cls(
            identity=data["identity"],
            document_id=data["document_id"],
            title=data.get(
                "title",
                "",
            ),
            text=data.get(
                "text",
                "",
            ),
            claims=[
                Claim.from_dict(claim)
                for claim in data.get(
                    "claims",
                    [],
                )
            ],
        )

    def __str__(self):
        if self.title:
            return (
                f"{self.identity} - "
                f"{self.title}"
            )

        return self.identity