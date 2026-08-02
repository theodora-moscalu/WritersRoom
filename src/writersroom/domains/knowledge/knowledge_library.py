from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)


class KnowledgeLibrary:
    """Represents a collection of knowledge sources."""

    def __init__(
        self,
        knowledge_sources: list[KnowledgeSource] | None = None,
    ):
        self.knowledge_sources = (
            knowledge_sources or []
        )

    def to_dict(self):
        """Convert the knowledge library to a dictionary."""

        return {
            "knowledge_sources": [
                source.to_dict()
                for source in self.knowledge_sources
            ]
        }

    @classmethod
    def from_dict(cls, data):
        """Create a KnowledgeLibrary from a dictionary."""

        return cls(
            knowledge_sources=[
                KnowledgeSource.from_dict(source)
                for source in data.get(
                    "knowledge_sources",
                    [],
                )
            ]
        )

    def add_source(
        self,
        knowledge_source: KnowledgeSource,
    ):
        """Add a knowledge source."""

        self.knowledge_sources.append(
            knowledge_source
        )

    def remove_source(
        self,
        identity: str,
    ):
        """Remove a knowledge source."""

        self.knowledge_sources = [
            source
            for source in self.knowledge_sources
            if source.identity != identity
        ]

    def find_source(
        self,
        identity: str,
    ):
        """Find a knowledge source by identity."""

        for source in self.knowledge_sources:
            if source.identity == identity:
                return source

        return None

    def find_source_by_name(
        self,
        name: str,
    ):
        """Find a knowledge source by name."""

        for source in self.knowledge_sources:
            if (
                source.name.lower()
                == name.lower()
            ):
                return source

        return None

    def __iter__(self):
        return iter(
            self.knowledge_sources
        )

    def __len__(self):
        return len(
            self.knowledge_sources
        )