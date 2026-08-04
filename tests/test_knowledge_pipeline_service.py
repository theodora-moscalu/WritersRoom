from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_pipeline_service import (
    KnowledgePipelineService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def main():

    print(
        "Testing KnowledgePipelineService..."
    )

    workspace = Workspace()

    knowledge_service = (
        KnowledgeSourceService(
            workspace
        )
    )

    document_service = (
        DocumentService(
            workspace
        )
    )

    passage_service = (
        PassageService(
            workspace
        )
    )

    claim_service = (
        ClaimService(
            workspace
        )
    )

    knowledge_service.add_source(
        name="Story",
        source_type=(
            KnowledgeSourceType.BOOK
        ),
    )

    document_service.add_document(
        knowledge_source_name="Story",
        name="Story Guide",
    )

    passage_service.add_passage(
        knowledge_source_name="Story",
        document_name="Story Guide",
        text=(
            "Conflict creates drama."
        ),
    )

    processed_document = (
        ProcessedDocument(
            source_units=[
                SourceUnit(
                    sequence=1,
                    text=(
                        "Conflict creates drama."
                    ),
                    unit_type=(
                        SourceUnitType.PARAGRAPH
                    ),
                )
            ]
        )
    )

    pipeline = (
        KnowledgePipelineService(
            workspace
        )
    )

    result = pipeline.process(
        knowledge_source_name="Story",
        document_name="Story Guide",
        processed_document=(
            processed_document
        ),
    )

    assert (
        len(result.accepted_items)
        >= 1
    )

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
        >= 1
    )

    claim = claims.data[0]

    assert (
        claim.text
        != ""
    )

    assert (
        claim.explanation
        != ""
    )

    assert (
        claim.knowledge_level
        is not None
    )

    assert (
        claim.knowledge_domain
        is not None
    )

    assert (
        len(
            claim.provenance
        )
        == 1
    )

    print()

    print(
        "Stored claim:"
    )

    print()

    print(
        f"Level: {claim.knowledge_level}"
    )

    print(
        f"Domain: {claim.knowledge_domain}"
    )

    print()

    print(
        claim.text
    )

    print()

    print(
        "KnowledgePipelineService tests passed."
    )


if __name__ == "__main__":
    main()