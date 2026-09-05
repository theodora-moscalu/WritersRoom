from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)


def main():
    print("Testing KnowledgeSource...")

    source = KnowledgeSource(
        identity="KS000001",
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
        author="Robert McKee",
        description="Classic book on screenwriting.",
    )

    assert source.identity.startswith("KS")

    assert source.name == "Story"

    assert (
        source.source_type
        == KnowledgeSourceType.BOOK
    )

    data = source.to_dict()

    loaded = KnowledgeSource.from_dict(data)

    assert loaded.identity == source.identity
    assert loaded.name == source.name
    assert (
        loaded.source_type
        == source.source_type
    )
    assert loaded.author == source.author
    assert (
        loaded.description
        == source.description
    )

    print("KnowledgeSource tests passed.")


if __name__ == "__main__":
    main()
