from support import knowledge_repository

from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)


def main():
    print("Testing KnowledgeSourceService...")

    repository = knowledge_repository()

    service = KnowledgeSourceService(
        repository
    )

    #
    # Add
    #

    result = service.add_source(
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
        author="Robert McKee",
        description="Classic screenwriting book.",
    )

    assert result.success

    source = result.data

    assert source.name == "Story"
    assert (
        source.source_type
        == KnowledgeSourceType.BOOK
    )

    assert source.author == "Robert McKee"

    assert (
        repository.get_source_by_name(
            "Story"
        ).identity
        == source.identity
    )

    #
    # Duplicate
    #

    result = service.add_source(
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
    )

    assert not result.success

    #
    # List
    #

    result = service.list_sources()

    assert result.success

    assert len(result.data) == 1

    #
    # Show
    #

    result = service.show_source(
        "Story"
    )

    assert result.success

    assert (
        result.data.identity
        == source.identity
    )

    #
    # Delete
    #

    result = service.delete_source(
        "Story"
    )

    assert result.success

    assert (
        repository.get_source_by_name(
            "Story"
        )
        is None
    )

    print(
        "KnowledgeSourceService tests passed."
    )


if __name__ == "__main__":
    main()
