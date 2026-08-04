from writersroom.common.result import Result
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.document import (
    Document,
)


class DocumentService:
    """Business logic for documents."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

    def add_document(
        self,
        knowledge_source_name: str,
        name: str,
        description: str = "",
    ) -> Result:
        """Create a document."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
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
            knowledge_source.find_document(
                name
            )
            is not None
        ):
            return Result.fail(
                f"Document '{name}' already exists."
            )

        document = Document(
            identity=self.workspace.generate_identity(
                IdentityPrefix.DOCUMENT
            ),
            knowledge_source_id=(
                knowledge_source.identity
            ),
            name=name,
            description=description,
        )

        knowledge_source.add_document(
            document
        )

        self.workspace.save()

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
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        return Result.ok(
            data=knowledge_source.list_documents(),
        )

    def show_document(
        self,
        knowledge_source_name: str,
        name: str,
    ) -> Result:
        """Return a document."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = (
            knowledge_source.find_document(
                name
            )
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

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = (
            knowledge_source.find_document(
                name
            )
        )

        if document is None:
            return Result.fail(
                f"Document '{name}' was not found."
            )

        knowledge_source.remove_document(
            name
        )

        self.workspace.save()

        return Result.ok(
            f"Deleted document '{name}'."
        )