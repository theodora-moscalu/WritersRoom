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

    def __init__(self, repository, project_id=None):
        self.repository = repository
        self.project_id = project_id

    def add_source(
        self,
        name: str,
        source_type: KnowledgeSourceType,
        author: str = "",
        description: str = "",
        tier: str = "writing",
    ) -> Result:
        """Create a knowledge source in a tier (writing is shared)."""

        name = name.strip()

        if not name:
            return Result.fail(
                "Knowledge source name cannot be empty."
            )

        if tier == "general" and self.project_id is None:
            return Result.fail(
                "General knowledge needs an open workspace."
            )

        if (
            self.repository.get_source_by_name(
                name,
                self.project_id,
            )
            is not None
        ):
            return Result.fail(
                f"Knowledge source '{name}' already exists."
            )

        source = KnowledgeSource(
            identity=self.repository.next_identity(
                IdentityPrefix.KNOWLEDGE_SOURCE
            ),
            name=name,
            source_type=source_type,
            author=author,
            description=description,
        )

        self.repository.add_source(
            source,
            tier=tier,
            project_id=self.project_id,
        )

        return Result.ok(
            f"Added knowledge source '{name}'.",
            data=source,
        )

    def list_sources(self) -> Result:
        """Return the knowledge sources visible to the current workspace."""

        return Result.ok(
            data=self.repository.list_sources(
                self.project_id
            )
        )

    def show_source(
        self,
        name: str,
    ) -> Result:
        """Return a knowledge source."""

        source = self.repository.get_source_by_name(
            name,
            self.project_id,
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

        source = self.repository.get_source_by_name(
            name,
            self.project_id,
        )

        if source is None:
            return Result.fail(
                f"Knowledge source '{name}' was not found."
            )

        self.repository.delete_source(
            source.identity
        )

        return Result.ok(
            f"Deleted knowledge source '{name}'."
        )
