class Provenance:
    """Represents the provenance of a knowledge claim."""

    def __init__(
        self,
        identity: str,
        claim_id: str,
        source_document_id: str,
        passage_id: str,
        confidence: float = 1.0,
        reviewed: bool = False,
    ):
        self.identity = identity
        self.claim_id = claim_id
        self.source_document_id = (
            source_document_id
        )
        self.passage_id = passage_id
        self.confidence = confidence
        self.reviewed = reviewed

    def to_dict(self):
        """Convert the provenance to a dictionary."""

        return {
            "identity": self.identity,
            "claim_id": self.claim_id,
            "source_document_id": (
                self.source_document_id
            ),
            "passage_id": self.passage_id,
            "confidence": self.confidence,
            "reviewed": self.reviewed,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Provenance from a dictionary."""

        return cls(
            identity=data["identity"],
            claim_id=data["claim_id"],
            source_document_id=data[
                "source_document_id"
            ],
            passage_id=data["passage_id"],
            confidence=data.get(
                "confidence",
                1.0,
            ),
            reviewed=data.get(
                "reviewed",
                False,
            ),
        )

    def __str__(self):
        return (
            f"{self.identity} "
            f"(confidence={self.confidence:.2f})"
        )