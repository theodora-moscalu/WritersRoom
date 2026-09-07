from writersroom.common.result import Result
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.document import (
    Document,
)


class DocumentService:
    """Business logic for documents."""

    def __init__(self, repository, project_id=None):
        self.repository = repository
        self.project_id = project_id

    def add_document(
        self,
        knowledge_source_name: str,
        name: str,
        description: str = "",
    ) -> Result:
        """Create a document."""

        knowledge_source = (
            self.repository.get_source_by_name(
                knowledge_source_name,
                self.project_id,
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        name = name.strip()

        if not name:
            return Result.fail(
                "Document name cannot be empty."
            )

        if (
            self.repository.get_document_by_name(
                knowledge_source.identity,
                name,
            )
            is not None
        ):
            return Result.fail(
                f"Document '{name}' already exists."
            )

        document = Document(
            identity=self.repository.next_identity(
                IdentityPrefix.DOCUMENT
            ),
            knowledge_source_id=(
                knowledge_source.identity
            ),
            name=name,
            description=description,
        )

        self.repository.add_document(document)

        return Result.ok(
            f"Added document '{name}'.",
            data=document,
        )

    def list_documents(
        self,
        knowledge_source_name: str,
    ) -> Result:
        """Return all documents."""

        knowledge_source = (
            self.repository.get_source_by_name(
                knowledge_source_name,
                self.project_id,
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        return Result.ok(
            data=self.repository.list_documents(
                knowledge_source.identity
            ),
        )

    def show_document(
        self,
        knowledge_source_name: str,
        name: str,
    ) -> Result:
        """Return a document."""

        document = self._find_document(
            knowledge_source_name,
            name,
        )

        if document is None:
            return Result.fail(
                f"Document '{name}' was not found."
            )

        return Result.ok(
            data=document,
        )

    def delete_document(
        self,
        knowledge_source_name: str,
        name: str,
    ) -> Result:
        """Delete a document."""

        document = self._find_document(
            knowledge_source_name,
            name,
        )

        if document is None:
            return Result.fail(
                f"Document '{name}' was not found."
            )

        self.repository.delete_document(
            document.identity
        )

        return Result.ok(
            f"Deleted document '{name}'."
        )

    def _find_document(
        self,
        knowledge_source_name: str,
        name: str,
    ):
        """Resolve a document by source name and document name."""

        knowledge_source = (
            self.repository.get_source_by_name(
                knowledge_source_name,
                self.project_id,
            )
        )

        if knowledge_source is None:
            return None

        return self.repository.get_document_by_name(
            knowledge_source.identity,
            name,
        )
