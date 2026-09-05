from support import knowledge_repository

from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extracted_provenance import (
    ExtractedProvenance,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def main():
    print("Testing ClaimService...")

    repository = knowledge_repository()

    knowledge_service = (
        KnowledgeSourceService(
            repository
        )
    )

    document_service = (
        DocumentService(
            repository
        )
    )

    passage_service = (
        PassageService(
            repository
        )
    )

    claim_service = (
        ClaimService(
            repository
        )
    )

    knowledge_service.add_source(
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
    )

    document_service.add_document(
        knowledge_source_name="Story",
        name="Story Guide",
    )

    passage_service.add_passage(
        knowledge_source_name="Story",
        document_name="Story Guide",
        text=(
            "A protagonist should pursue "
            "a concrete objective."
        ),
    )

    extracted = ExtractedClaim(
        text=(
            "A protagonist should pursue "
            "a concrete objective."
        ),
        knowledge_level=KnowledgeLevel.PRINCIPLE,
        knowledge_domain=KnowledgeDomain.STRUCTURE,
        explanation=(
            "Objectives create momentum."
        ),
        provenance=[
            ExtractedProvenance(
                passage_sequence=1,
                confidence=0.95,
            )
        ],
    )

    result = (
        claim_service.add_extracted_claim(
            knowledge_source_name="Story",
            document_name="Story Guide",
            extracted=extracted,
        )
    )

    assert result.success

    claims = (
        claim_service.list_claims(
            "Story",
            "Story Guide",
            1,
        )
    )

    assert claims.success

    assert (
        len(claims.data)
        == 1
    )

    claim = claims.data[0]

    assert (
        claim.text
        == (
            "A protagonist should pursue "
            "a concrete objective."
        )
    )

    assert (
        claim.explanation
        == (
            "Objectives create momentum."
        )
    )

    assert (
        len(claim.provenance)
        == 1
    )

    assert (
        claim.provenance[0].confidence
        == 0.95
    )

    print(
        "ClaimService tests passed."
    )


if __name__ == "__main__":
    main()