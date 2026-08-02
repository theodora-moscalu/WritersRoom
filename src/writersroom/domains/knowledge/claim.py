from writersroom.domains.knowledge.citation import (
    Citation,
)


class Claim:
    """Represents a single knowledge claim extracted from a passage."""

    def __init__(
        self,
        identity: str,
        passage_id: str,
        text: str,
        explanation: str = "",
        tags: list[str] | None = None,
        citations: list[Citation] | None = None,
    ):
        self.identity = identity
        self.passage_id = passage_id
        self.text = text
        self.explanation = explanation
        self.tags = tags or []
        self.citations = citations or []

    def to_dict(self):
        """Convert the claim to a dictionary."""

        return {
            "identity": self.identity,
            "passage_id": self.passage_id,
            "text": self.text,
            "explanation": self.explanation,
            "tags": self.tags,
            "citations": [
                citation.to_dict()
                for citation in self.citations
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Claim from a dictionary."""

        return cls(
            identity=data["identity"],
            passage_id=data["passage_id"],
            text=data["text"],
            explanation=data.get(
                "explanation",
                "",
            ),
            tags=data.get(
                "tags",
                [],
            ),
            citations=[
                Citation.from_dict(citation)
                for citation in data.get(
                    "citations",
                    [],
                )
            ],
        )

    def __str__(self):
        return (
            f"{self.identity} - "
            f"{self.text}"
        )