from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)
from writersroom.domains.knowledge.provenance import (
    Provenance,
)
from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)


class ClaimMapper:
    """Maps extracted claims into domain claims."""

    @staticmethod
    def map(
        workspace,
        passage: Passage,
        extracted: ExtractedClaim,
    ) -> Claim:
        """Create a domain claim."""

        claim = Claim(
            identity=workspace.generate_identity(
                IdentityPrefix.CLAIM
            ),
            passage_id=passage.identity,
            text=extracted.text,
            knowledge_level=(
                extracted.knowledge_level
            ),
            knowledge_domain=(
                extracted.knowledge_domain
            ),
            explanation=(
                extracted.explanation
            ),
        )

        for item in extracted.provenance:

            claim.add_provenance(
                Provenance(
                    identity=workspace.generate_identity(
                        IdentityPrefix.PROVENANCE
                    ),
                    claim_id=claim.identity,
                    source_document_id=(
                        passage.document_id
                    ),
                    passage_id=passage.identity,
                    confidence=item.confidence,
                    reviewed=True,
                )
            )

        return claim