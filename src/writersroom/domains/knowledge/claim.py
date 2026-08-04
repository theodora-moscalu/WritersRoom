from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.knowledge.provenance import (
    Provenance,
)


class Claim:
    """Represents accepted storytelling knowledge."""

    def __init__(
        self,
        identity: str,
        passage_id: str,
        text: str,
        knowledge_level: KnowledgeLevel,
        knowledge_domain: KnowledgeDomain,
        explanation: str = "",
        provenance: list[Provenance] | None = None,
    ):
        self.identity = identity

        self.passage_id = passage_id

        self.text = text

        self.knowledge_level = (
            knowledge_level
        )

        self.knowledge_domain = (
            knowledge_domain
        )

        self.explanation = explanation

        self.provenance = (
            provenance or []
        )

    def to_dict(self):
        """Convert the claim to a dictionary."""

        return {
            "identity": self.identity,
            "passage_id": self.passage_id,
            "text": self.text,
            "knowledge_level": (
                self.knowledge_level.value
            ),
            "knowledge_domain": (
                self.knowledge_domain.value
            ),
            "explanation": (
                self.explanation
            ),
            "provenance": [
                item.to_dict()
                for item in self.provenance
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data,
    ):
        """Create a Claim from a dictionary."""

        return cls(
            identity=data["identity"],
            passage_id=data["passage_id"],
            text=data["text"],
            knowledge_level=(
                KnowledgeLevel(
                    data[
                        "knowledge_level"
                    ]
                )
            ),
            knowledge_domain=(
                KnowledgeDomain(
                    data[
                        "knowledge_domain"
                    ]
                )
            ),
            explanation=data.get(
                "explanation",
                "",
            ),
            provenance=[
                Provenance.from_dict(
                    item
                )
                for item in data.get(
                    "provenance",
                    [],
                )
            ],
        )

    def add_provenance(
        self,
        provenance: Provenance,
    ):
        """Add provenance."""

        self.provenance.append(
            provenance
        )

    def remove_provenance(
        self,
        identity: str,
    ):
        """Remove provenance."""

        self.provenance = [
            item
            for item in self.provenance
            if item.identity
            != identity
        ]

    def find_provenance(
        self,
        identity: str,
    ):
        """Find provenance."""

        for item in self.provenance:

            if (
                item.identity
                == identity
            ):
                return item

        return None

    def list_provenance(
        self,
    ):
        """Return provenance."""

        return self.provenance

    def __str__(
        self,
    ):
        return (
            f"{self.identity} "
            f"[{self.knowledge_domain.name}/"
            f"{self.knowledge_level.name}] "
            f"{self.text}"
        )