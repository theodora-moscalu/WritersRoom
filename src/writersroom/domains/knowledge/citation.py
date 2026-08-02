class Citation:
    """Represents evidence supporting a knowledge claim."""

    def __init__(
        self,
        identity: str,
        claim_id: str,
        source_document_id: str,
        location: str = "",
        excerpt: str = "",
    ):
        self.identity = identity
        self.claim_id = claim_id
        self.source_document_id = (
            source_document_id
        )
        self.location = location
        self.excerpt = excerpt

    def to_dict(self):
        """Convert the citation to a dictionary."""

        return {
            "identity": self.identity,
            "claim_id": self.claim_id,
            "source_document_id": (
                self.source_document_id
            ),
            "location": self.location,
            "excerpt": self.excerpt,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Citation from a dictionary."""

        return cls(
            identity=data["identity"],
            claim_id=data["claim_id"],
            source_document_id=data[
                "source_document_id"
            ],
            location=data.get(
                "location",
                "",
            ),
            excerpt=data.get(
                "excerpt",
                "",
            ),
        )

    def __str__(self):
        if self.location:
            return (
                f"{self.identity} "
                f"({self.location})"
            )

        return self.identity