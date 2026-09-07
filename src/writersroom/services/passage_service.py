from writersroom.common.result import Result
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)


class PassageService:
    """Business logic for passages."""

    def __init__(self, repository, project_id=None):
        self.repository = repository
        self.project_id = project_id

    def add_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        text: str,
    ) -> Result:
        """Create a passage."""

        document = self._find_document(
            knowledge_source_name,
            document_name,
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        sequence = (
            self.repository.next_passage_sequence(
                document.identity
            )
        )

        passage = Passage(
            identity=self.repository.next_identity(
                IdentityPrefix.PASSAGE
            ),
            document_id=document.identity,
            sequence=sequence,
            text=text,
        )

        self.repository.add_passage(passage)

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

        document = self._find_document(
            knowledge_source_name,
            document_name,
        )

        if document is None:
            return Result.fail(
                f"Document '{document_name}' was not found."
            )

        return Result.ok(
            data=self.repository.list_passages(
                document.identity
            ),
        )

    def show_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        sequence: int,
    ) -> Result:
        """Return a passage."""

        passage = self._find_passage(
            knowledge_source_name,
            document_name,
            sequence,
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

        passage = self._find_passage(
            knowledge_source_name,
            document_name,
            sequence,
        )

        if passage is None:
            return Result.fail(
                f"Passage {sequence} was not found."
            )

        self.repository.delete_passage(
            passage.identity
        )

        return Result.ok(
            f"Deleted passage {sequence}."
        )

    def _find_document(
        self,
        knowledge_source_name: str,
        document_name: str,
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
            document_name,
        )

    def _find_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        sequence: int,
    ):
        """Resolve a passage by source name, document name and sequence."""

        document = self._find_document(
            knowledge_source_name,
            document_name,
        )

        if document is None:
            return None

        return self.repository.get_passage_by_sequence(
            document.identity,
            sequence,
        )
