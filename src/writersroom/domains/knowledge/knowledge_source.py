from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.document import (
    Document,
)


class KnowledgeSource:
    """Represents a single source of writing knowledge."""

    def __init__(
        self,
        identity: str,
        name: str,
        source_type: KnowledgeSourceType,
        author: str = "",
        description: str = "",
        documents: list[Document] | None = None,
    ):
        self.identity = identity
        self.name = name
        self.source_type = source_type
        self.author = author
        self.description = description
        self.documents = documents or []

    def to_dict(self):
        """Convert the knowledge source to a dictionary."""

        return {
            "identity": self.identity,
            "name": self.name,
            "source_type": self.source_type.value,
            "author": self.author,
            "description": self.description,
            "documents": [
                document.to_dict()
                for document in self.documents
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a KnowledgeSource from a dictionary."""

        return cls(
            identity=data["identity"],
            name=data["name"],
            source_type=KnowledgeSourceType(
                data["source_type"]
            ),
            author=data.get("author", ""),
            description=data.get(
                "description",
                "",
            ),
            documents=[
                Document.from_dict(document)
                for document in data.get(
                    "documents",
                    [],
                )
            ],
        )

    #
    # Document methods
    #

    def add_document(
        self,
        document: Document,
    ):
        """Add a document."""

        self.documents.append(document)

    def find_document(
        self,
        name: str,
    ):
        """Find a document by name."""

        for document in self.documents:
            if (
                document.name.lower()
                == name.lower()
            ):
                return document

        return None

    def remove_document(
        self,
        name: str,
    ):
        """Remove a document."""

        document = self.find_document(
            name
        )

        if document is not None:
            self.documents.remove(document)

    def list_documents(self):
        """Return all documents."""

        return self.documents

    def __str__(self):
        return (
            f"{self.identity} - "
            f"{self.name}"
        )