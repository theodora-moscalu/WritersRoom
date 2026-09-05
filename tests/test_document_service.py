from support import knowledge_repository

from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)


def main():
    print("Testing DocumentService...")

    repository = knowledge_repository()

    knowledge_service = (
        KnowledgeSourceService(
            repository
        )
    )

    knowledge_service.add_source(
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
        author="Robert McKee",
    )

    document_service = DocumentService(
        repository
    )

    #
    # Add
    #

    result = document_service.add_document(
        knowledge_source_name="Story",
        name="Chapter 1",
        description="Opening chapter.",
    )

    assert result.success

    document = result.data

    assert document.name == "Chapter 1"

    source = repository.get_source_by_name(
        "Story"
    )

    assert (
        repository.get_document_by_name(
            source.identity,
            "Chapter 1",
        ).identity
        == document.identity
    )

    #
    # Duplicate
    #

    result = document_service.add_document(
        knowledge_source_name="Story",
        name="Chapter 1",
    )

    assert not result.success

    #
    # Empty name
    #

    result = document_service.add_document(
        knowledge_source_name="Story",
        name="",
    )

    assert not result.success

    #
    # Missing knowledge source
    #

    result = document_service.add_document(
        knowledge_source_name="Unknown",
        name="Chapter X",
    )

    assert not result.success

    #
    # List
    #

    result = document_service.list_documents(
        "Story"
    )

    assert result.success

    assert len(result.data) == 1

    #
    # Show
    #

    result = document_service.show_document(
        "Story",
        "Chapter 1",
    )

    assert result.success

    assert (
        result.data.identity
        == document.identity
    )

    #
    # Delete
    #

    result = document_service.delete_document(
        "Story",
        "Chapter 1",
    )

    assert result.success

    assert (
        repository.get_document_by_name(
            source.identity,
            "Chapter 1",
        )
        is None
    )

    print(
        "DocumentService tests passed."
    )


if __name__ == "__main__":
    main()
