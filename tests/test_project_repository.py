from writersroom.database.database import Database
from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)
from writersroom.database.project_repository import (
    ProjectRepository,
)
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.domains.story.character import (
    Character,
)


def main():
    print("Testing ProjectRepository...")

    database = Database(":memory:")
    projects = ProjectRepository(database)
    knowledge = KnowledgeRepository(database)

    wine = projects.create("The Wine Game")

    assert wine.identity.startswith("PR")
    assert wine.created is not None

    #
    # Blob round-trip
    #

    wine.add_character(
        Character(name="Zoe", description="A sommelier.")
    )
    wine.draft_path = "C:/scripts/wine.fountain"
    projects.save(wine)

    reloaded = projects.get(wine.identity)

    assert reloaded.title == "The Wine Game"
    assert len(reloaded.characters) == 1
    assert reloaded.characters[0].name == "Zoe"
    assert reloaded.draft_path == "C:/scripts/wine.fountain"

    #
    # Lookup and listing
    #

    projects.create("Constantinople")

    assert projects.get_by_title("constantinople") is not None
    assert len(projects.list()) == 2

    #
    # Rename
    #

    projects.rename(wine.identity, "The Wine Game (S1)")
    assert projects.get(wine.identity).title == "The Wine Game (S1)"

    #
    # Deleting a project cascades its general-tier knowledge
    #

    source = KnowledgeSource(
        identity=knowledge.next_identity(
            IdentityPrefix.KNOWLEDGE_SOURCE
        ),
        name="Wine Fraud",
        source_type=KnowledgeSourceType.RESEARCH_PAPER,
    )
    knowledge.add_source(
        source,
        tier="general",
        project_id=wine.identity,
    )

    assert len(knowledge.list_sources(wine.identity)) == 1

    projects.delete(wine.identity)

    assert projects.get(wine.identity) is None
    assert knowledge.get_source(source.identity) is None

    print()
    print("ProjectRepository tests passed.")


if __name__ == "__main__":
    main()
