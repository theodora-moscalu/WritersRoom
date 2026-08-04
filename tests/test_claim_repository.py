from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.retrieval.claim_repository import (
    ClaimRepository,
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

    print(
        "Testing ClaimRepository..."
    )

    workspace = Workspace()

    knowledge_sources = (
        KnowledgeSourceService(
            workspace
        )
    )

    documents = (
        DocumentService(
            workspace
        )
    )

    passages = (
        PassageService(
            workspace
        )
    )

    claims = (
        ClaimService(
            workspace
        )
    )

    knowledge_sources.add_source(
        name="Book",
        source_type=(
            KnowledgeSourceType.BOOK
        ),
    )

    documents.add_document(
        knowledge_source_name="Book",
        name="Story",
    )

    passages.add_passage(
        knowledge_source_name="Book",
        document_name="Story",
        text="Conflict creates drama.",
    )

    claims.add_claim(
        knowledge_source_name="Book",
        document_name="Story",
        passage_sequence=1,
        text="Conflict creates drama.",
        knowledge_level=(
            KnowledgeLevel.PRINCIPLE
        ),
        knowledge_domain=(
            KnowledgeDomain.CONFLICT
        ),
        explanation=(
            "Conflict drives narrative."
        ),
    )

    repository = (
        ClaimRepository(
            workspace
        )
    )

    all_claims = (
        repository.list_claims()
    )

    assert (
        len(all_claims)
        == 1
    )

    claim = all_claims[0]

    found = (
        repository.find_claim(
            claim.identity
        )
    )

    assert (
        found
        is not None
    )

    assert (
        found.identity
        == claim.identity
    )

    assert (
        found.text
        == "Conflict creates drama."
    )

    assert (
        found.knowledge_level
        == KnowledgeLevel.PRINCIPLE
    )

    assert (
        found.knowledge_domain
        == KnowledgeDomain.CONFLICT
    )

    print()

    print(
        f"Repository contains {len(all_claims)} claim(s)."
    )

    print()

    print(
        "ClaimRepository tests passed."
    )


if __name__ == "__main__":
    main()