from pathlib import Path

from support import knowledge_repository

from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.services.import_service import (
    ImportService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)


def main():
    print("Testing ImportService...")

    repository = knowledge_repository()

    knowledge_service = (
        KnowledgeSourceService(
            repository
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
            repository
        )
    )

    result = (
        import_service.import_document(
        knowledge_source_name="Books",
        knowledge_source_type=KnowledgeSourceType.BOOK,
        path=str(test_file),
        document_name="Test Story",
        )
    )

    assert result.success

    source = repository.get_source_by_name(
        "Books"
    )

    assert source is not None

    document = repository.get_document_by_name(
        source.identity,
        "Test Story",
    )

    assert document is not None

    passages = repository.list_passages(
        document.identity
    )

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

    #
    # General-tier import: passages are stored, no extraction runs
    #

    from writersroom.database.project_repository import (
        ProjectRepository,
    )
    from writersroom.services.import_service import ImportService as _IS

    project = ProjectRepository(
        repository.database
    ).create("The Wine Game")

    general_import = _IS(repository, project.identity)

    world_file = Path("tests/world.txt")
    world_file.write_text(
        "Counterfeit Burgundy often has mismatched fill levels.",
        encoding="utf-8",
    )

    result = general_import.import_document(
        knowledge_source_name="Wine Fraud",
        knowledge_source_type=KnowledgeSourceType.RESEARCH_PAPER,
        path=str(world_file),
        document_name="Notes",
        tier="general",
    )

    assert result.success
    assert "not enabled yet" in result.message

    source = repository.get_source_by_name(
        "Wine Fraud", project.identity
    )
    assert source.tier == "general"
    assert len(
        repository.list_passages(
            repository.get_document_by_name(
                source.identity, "Notes"
            ).identity
        )
    ) == 1

    world_file.unlink()
    test_file.unlink()

    print(
        "ImportService tests passed."
    )


if __name__ == "__main__":
    main()
