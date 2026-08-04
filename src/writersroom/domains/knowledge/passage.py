from writersroom.domains.knowledge.claim import (
    Claim,
)


class Passage:
    """Represents a contiguous passage within a document."""

    def __init__(
        self,
        identity: str,
        document_id: str,
        sequence: int,
        text: str = "",
        claims: list[Claim] | None = None,
    ):
        self.identity = identity
        self.document_id = document_id
        self.sequence = sequence
        self.text = text
        self.claims = claims or []

    def to_dict(self):
        """Convert the passage to a dictionary."""

        return {
            "identity": self.identity,
            "document_id": self.document_id,
            "sequence": self.sequence,
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
            sequence=data["sequence"],
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

    def add_claim(
        self,
        claim: Claim,
    ):
        """Add a claim."""

        self.claims.append(claim)

    def find_claim(
        self,
        identity: str,
    ):
        """Find a claim by identity."""

        for claim in self.claims:
            if claim.identity == identity:
                return claim

        return None

    def remove_claim(
        self,
        identity: str,
    ):
        """Remove a claim."""

        claim = self.find_claim(
            identity
        )

        if claim is not None:
            self.claims.remove(
                claim
            )

    def list_claims(self):
        """Return all claims."""

        return self.claims

    def __str__(self):
        return (
            f"Passage {self.sequence}"
        )