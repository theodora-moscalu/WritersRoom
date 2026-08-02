from writersroom.domains.knowledge.passage import (
    Passage,
)


class Document:
    """Represents a document within a knowledge source."""

    def __init__(
        self,
        identity: str,
        knowledge_source_id: str,
        name: str,
        description: str = "",
        passages: list[Passage] | None = None,
    ):
        self.identity = identity
        self.knowledge_source_id = (
            knowledge_source_id
        )
        self.name = name
        self.description = description
        self.passages = passages or []

    def to_dict(self):
        """Convert the document to a dictionary."""

        return {
            "identity": self.identity,
            "knowledge_source_id": (
                self.knowledge_source_id
            ),
            "name": self.name,
            "description": self.description,
            "passages": [
                passage.to_dict()
                for passage in self.passages
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Document from a dictionary."""

        return cls(
            identity=data["identity"],
            knowledge_source_id=data[
                "knowledge_source_id"
            ],
            name=data["name"],
            description=data.get(
                "description",
                "",
            ),
            passages=[
                Passage.from_dict(passage)
                for passage in data.get(
                    "passages",
                    [],
                )
            ],
        )

    def __str__(self):
        return (
            f"{self.identity} - "
            f"{self.name}"
        )