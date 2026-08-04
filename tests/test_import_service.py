from pathlib import Path

from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import Workspace
from writersroom.services.import_service import (
    ImportService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)


def main():
    print("Testing ImportService...")

    workspace = Workspace()

    knowledge_service = (
        KnowledgeSourceService(
            workspace
        )
    )

    knowledge_service.add_source(
        name="Books",
        source_type=KnowledgeSourceType.BOOK,
    )

    test_file = Path(
        "tests/story.txt"
    )

    test_file.write_text(
        (
            "Chapter 1\n\n"
            "A protagonist should pursue "
            "a concrete objective.\n\n"
            "Every scene should contain conflict."
        ),
        encoding="utf-8",
    )

    import_service = (
        ImportService(
            workspace
        )
    )

    result = import_service.import_document(
        "Books",
        str(test_file),
    )

    assert result.success

    source = (
        workspace.find_knowledge_source_by_name(
            "Books"
        )
    )

    assert source is not None

    document = source.find_document(
        "story"
    )

    assert document is not None

    passages = document.list_passages()

    assert len(passages) == 3

    assert (
        passages[0].sequence
        == 1
    )

    assert (
        passages[0].text
        == "Chapter 1"
    )

    assert (
        passages[1].sequence
        == 2
    )

    assert (
        passages[1].text
        == (
            "A protagonist should pursue "
            "a concrete objective."
        )
    )

    assert (
        passages[2].sequence
        == 3
    )

    assert (
        passages[2].text
        == (
            "Every scene should contain conflict."
        )
    )

    test_file.unlink()

    print(
        "ImportService tests passed."
    )


if __name__ == "__main__":
    main()