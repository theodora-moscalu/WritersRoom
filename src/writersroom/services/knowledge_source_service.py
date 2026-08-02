from writersroom.common.result import Result
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)


class KnowledgeSourceService:
    """Business logic for knowledge sources."""

    def __init__(self, workspace):
        self.workspace = workspace

    def add_source(
        self,
        name: str,
        source_type: KnowledgeSourceType,
        author: str = "",
        description: str = "",
    ) -> Result:
        """Create a knowledge source."""

        name = name.strip()

        if not name:
            return Result.fail(
                "Knowledge source name cannot be empty."
            )

        if (
            self.workspace.find_knowledge_source_by_name(
                name
            )
            is not None
        ):
            return Result.fail(
                f"Knowledge source '{name}' already exists."
            )

        source = KnowledgeSource(
            identity=self.workspace.generate_identity(
                IdentityPrefix.KNOWLEDGE_SOURCE
            ),
            name=name,
            source_type=source_type,
            author=author,
            description=description,
        )

        self.workspace.add_knowledge_source(
            source
        )

        self.workspace.save()

        return Result.ok(
            f"Added knowledge source '{name}'.",
            data=source,
        )

    def list_sources(self) -> Result:
        """Return all knowledge sources."""

        return Result.ok(
            data=self.workspace.list_knowledge_sources()
        )

    def show_source(
        self,
        name: str,
    ) -> Result:
        """Return a knowledge source."""

        source = (
            self.workspace.find_knowledge_source_by_name(
                name
            )
        )

        if source is None:
            return Result.fail(
                f"Knowledge source '{name}' was not found."
            )

        return Result.ok(
            data=source,
        )

    def delete_source(
        self,
        name: str,
    ) -> Result:
        """Delete a knowledge source."""

        source = (
            self.workspace.find_knowledge_source_by_name(
                name
            )
        )

        if source is None:
            return Result.fail(
                f"Knowledge source '{name}' was not found."
            )

        self.workspace.remove_knowledge_source(
            source.identity
        )

        self.workspace.save()

        return Result.ok(
            f"Deleted knowledge source '{name}'."
        )