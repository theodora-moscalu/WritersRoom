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
from writersroom.review.review_result import (
    ReviewResult,
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

    assert isinstance(
        result,
        ReviewResult,
    )

    assert (
        len(result.items)
        >= 1
    )

    item = result.items[0]

    assert item.claim is not None

    assert (
        item.claim.text
        != ""
    )

    assert (
        item.claim.explanation
        != ""
    )

    assert (
        item.claim.knowledge_level
        is not None
    )

    assert (
        item.claim.knowledge_domain
        is not None
    )

    assert (
        len(
            item.claim.provenance
        )
        == 1
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
        == 0
    )

    print()

    print(
        "Review candidates:"
    )

    print()

    print(
        f"Candidates: "
        f"{len(result.items)}"
    )

    print()

    print(
        f"Level: "
        f"{item.claim.knowledge_level}"
    )

    print(
        f"Domain: "
        f"{item.claim.knowledge_domain}"
    )

    print()

    print(
        item.claim.text
    )

    print()

    print(
        "KnowledgePipelineService tests passed."
    )


if __name__ == "__main__":
    main()