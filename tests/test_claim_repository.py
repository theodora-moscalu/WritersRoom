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
        "Testing KnowledgeRepository..."
    )

    repository = knowledge_repository()

    KnowledgeSourceService(
        repository
    ).add_source(
        name="Book",
        source_type=(
            KnowledgeSourceType.BOOK
        ),
    )

    DocumentService(
        repository
    ).add_document(
        knowledge_source_name="Book",
        name="Story",
    )

    PassageService(
        repository
    ).add_passage(
        knowledge_source_name="Book",
        document_name="Story",
        text="Conflict creates drama.",
    )

    ClaimService(
        repository
    ).add_claim(
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

    all_claims = (
        repository.list_claims()
    )

    assert (
        len(all_claims)
        == 1
    )

    claim = all_claims[0]

    found = (
        repository.get_claim(
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

    #
    # Deletion cascades and reads survive a fresh repository view
    #

    repository.delete_claim(
        claim.identity
    )

    assert (
        repository.get_claim(
            claim.identity
        )
        is None
    )

    assert (
        len(repository.list_claims())
        == 0
    )

    print()

    print(
        "KnowledgeRepository tests passed."
    )


if __name__ == "__main__":
    main()
