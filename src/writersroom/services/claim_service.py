from writersroom.common.result import (
    Result,
)
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.mappers.claim_mapper import (
    ClaimMapper,
)


class ClaimService:
    """Business logic for claims."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

    def add_claim(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
        text: str,
        knowledge_level: KnowledgeLevel,
        knowledge_domain: KnowledgeDomain,
        explanation: str = "",
    ) -> Result:
        """Create a claim manually."""

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
            passage_sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        claim = Claim(
            identity=self.workspace.generate_identity(
                IdentityPrefix.CLAIM
            ),
            passage_id=passage.identity,
            text=text,
            knowledge_level=knowledge_level,
            knowledge_domain=knowledge_domain,
            explanation=explanation,
        )

        passage.add_claim(
            claim
        )

        self.workspace.save()

        return Result.ok(
            "Added claim.",
            data=claim,
        )

    def add_extracted_claim(
        self,
        knowledge_source_name: str,
        document_name: str,
        extracted: ExtractedClaim,
    ) -> Result:
        """Add an extracted claim."""

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

        if not extracted.provenance:
            return Result.fail(
                "Extracted claim has no provenance."
            )

        passage_sequence = (
            extracted.provenance[0]
            .passage_sequence
        )

        passage = document.find_passage(
            passage_sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        claim = ClaimMapper.map(
            workspace=self.workspace,
            passage=passage,
            extracted=extracted,
        )

        passage.add_claim(
            claim
        )

        self.workspace.save()

        return Result.ok(
            "Added extracted claim.",
            data=claim,
        )

    def list_claims(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
    ) -> Result:
        """Return all claims."""

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
            passage_sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        return Result.ok(
            data=passage.list_claims(),
        )

    def show_claim(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
        claim_identity: str,
    ) -> Result:
        """Return a claim."""

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
            passage_sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        claim = passage.find_claim(
            claim_identity
        )

        if claim is None:
            return Result.fail(
                f"Claim '{claim_identity}' was not found."
            )

        return Result.ok(
            data=claim,
        )

    def delete_claim(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
        claim_identity: str,
    ) -> Result:
        """Delete a claim."""

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
            passage_sequence
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        claim = passage.find_claim(
            claim_identity
        )

        if claim is None:
            return Result.fail(
                f"Claim '{claim_identity}' was not found."
            )

        passage.remove_claim(
            claim_identity
        )

        self.workspace.save()

        return Result.ok(
            "Deleted claim."
        )