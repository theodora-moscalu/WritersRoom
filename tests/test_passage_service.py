from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import Workspace
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
    print("Testing PassageService...")

    workspace = Workspace()

    knowledge_service = (
        KnowledgeSourceService(
            workspace
        )
    )

    knowledge_service.add_source(
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
    )

    document_service = (
        DocumentService(
            workspace
        )
    )

    document_service.add_document(
        knowledge_source_name="Story",
        name="Chapter 1",
    )

    passage_service = (
        PassageService(
            workspace
        )
    )

    #
    # Add
    #

    result = passage_service.add_passage(
        knowledge_source_name="Story",
        document_name="Chapter 1",
        text="This is the first passage.",
    )

    assert result.success

    passage = result.data

    assert passage.sequence == 1

    source = (
        workspace.find_knowledge_source_by_name(
            "Story"
        )
    )

    document = source.find_document(
        "Chapter 1"
    )

    assert (
        document.find_passage(1)
        is passage
    )

    #
    # Add second passage
    #

    result = passage_service.add_passage(
        knowledge_source_name="Story",
        document_name="Chapter 1",
        text="This is the second passage.",
    )

    assert result.success
    assert result.data.sequence == 2

    #
    # List
    #

    result = passage_service.list_passages(
        "Story",
        "Chapter 1",
    )

    assert result.success
    assert len(result.data) == 2

    #
    # Show
    #

    result = passage_service.show_passage(
        "Story",
        "Chapter 1",
        2,
    )

    assert result.success
    assert (
        result.data.text
        == "This is the second passage."
    )

    #
    # Delete
    #

    result = passage_service.delete_passage(
        "Story",
        "Chapter 1",
        1,
    )

    assert result.success

    assert (
        document.find_passage(1)
        is None
    )

    print(
        "PassageService tests passed."
    )


if __name__ == "__main__":
    main()