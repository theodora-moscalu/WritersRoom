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

    def __init__(self, repository, project_id=None):
        self.repository = repository
        self.project_id = project_id

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

        passage = self._find_passage(
            knowledge_source_name,
            document_name,
            passage_sequence,
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        claim = Claim(
            identity=self.repository.next_identity(
                IdentityPrefix.CLAIM
            ),
            passage_id=passage.identity,
            text=text,
            knowledge_level=knowledge_level,
            knowledge_domain=knowledge_domain,
            explanation=explanation,
        )

        self.repository.add_claim(claim)

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

        if not extracted.provenance:
            return Result.fail(
                "Extracted claim has no provenance."
            )

        passage = self._find_passage(
            knowledge_source_name,
            document_name,
            extracted.provenance[0].passage_sequence,
        )

        if passage is None:
            return Result.fail(
                "Passage "
                f"{extracted.provenance[0].passage_sequence} "
                "was not found."
            )

        claim = ClaimMapper.map(
            repository=self.repository,
            passage=passage,
            extracted=extracted,
        )

        self.repository.add_claim(claim)

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
        """Return all claims for a passage."""

        passage = self._find_passage(
            knowledge_source_name,
            document_name,
            passage_sequence,
        )

        if passage is None:
            return Result.fail(
                f"Passage {passage_sequence} was not found."
            )

        return Result.ok(
            data=self.repository.list_claims_for_passage(
                passage.identity
            ),
        )

    def show_claim(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
        claim_identity: str,
    ) -> Result:
        """Return a claim."""

        claim = self.repository.get_claim(
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

        claim = self.repository.get_claim(
            claim_identity
        )

        if claim is None:
            return Result.fail(
                f"Claim '{claim_identity}' was not found."
            )

        self.repository.delete_claim(
            claim_identity
        )

        return Result.ok(
            "Deleted claim."
        )

    def _find_passage(
        self,
        knowledge_source_name: str,
        document_name: str,
        passage_sequence: int,
    ):
        """Resolve a passage by source name, document name and sequence."""

        source = self.repository.get_source_by_name(
            knowledge_source_name,
            self.project_id,
        )

        if source is None:
            return None

        document = self.repository.get_document_by_name(
            source.identity,
            document_name,
        )

        if document is None:
            return None

        return self.repository.get_passage_by_sequence(
            document.identity,
            passage_sequence,
        )
