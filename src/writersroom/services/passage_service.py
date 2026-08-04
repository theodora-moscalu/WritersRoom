from writersroom.common.result import Result
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)


class PassageService:
    """Business logic for passages."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

    def add_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        text: str,
    ) -> Result:
        """Create a passage."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = knowledge_source.find_document(
            document_name
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        sequence = (
            document.next_passage_sequence()
        )

        passage = Passage(
            identity=self.workspace.generate_identity(
                IdentityPrefix.PASSAGE
            ),
            document_id=document.identity,
            sequence=sequence,
            text=text,
        )

        document.add_passage(
            passage
        )

        self.workspace.save()

        return Result.ok(
            f"Added passage {sequence}.",
            data=passage,
        )

    def list_passages(
        self,
        knowledge_source_name: str,
        document_name: str,
    ) -> Result:
        """Return all passages."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = knowledge_source.find_document(
            document_name
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        return Result.ok(
            data=document.list_passages(),
        )

    def show_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        sequence: int,
    ) -> Result:
        """Return a passage."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = knowledge_source.find_document(
            document_name
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        passage = document.find_passage(
            sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {sequence} was not found."
            )

        return Result.ok(
            data=passage,
        )

    def delete_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        sequence: int,
    ) -> Result:
        """Delete a passage."""

        knowledge_source = (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
        )

        if knowledge_source is None:
            return Result.fail(
                f"Knowledge source '{knowledge_source_name}' was not found."
            )

        document = knowledge_source.find_document(
            document_name
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        passage = document.find_passage(
            sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {sequence} was not found."
            )

        document.remove_passage(
            sequence
        )

        self.workspace.save()

        return Result.ok(
            f"Deleted passage {sequence}."
        )