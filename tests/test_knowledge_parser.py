from writersroom.domains.enums.importance import (
    Importance,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.parsers.knowledge_parser import (
    KnowledgeParser,
)


def main():

    print(
        "Testing KnowledgeParser..."
    )

    response = """
--------------------------------------------------

LEVEL:
OBSERVATION

DOMAIN:
CHARACTER

IMPORTANCE:
HIGH

TEXT:
The protagonist is introduced alone.

EXPLANATION:
The opening establishes isolation.

--------------------------------------------------

LEVEL:
TECHNIQUE

DOMAIN:
SCENE

IMPORTANCE:
MEDIUM

TEXT:
Open with action before exposition.

EXPLANATION:
Action creates immediate engagement.
"""

    parser = (
        KnowledgeParser()
    )

    records = parser.parse(
        response
    )

    print()

    print(
        f"Parsed {len(records)} records"
    )

    print()

    for index, record in enumerate(
        records,
        start=1,
    ):

        print(
            f"Record {index}"
        )

        print(record)

        print()

    assert (
        len(records)
        == 2
    )

    assert (
        records[0].knowledge_level
        == KnowledgeLevel.OBSERVATION
    )

    assert (
        records[0].knowledge_domain
        == KnowledgeDomain.CHARACTER
    )

    assert (
        records[0].importance
        == Importance.HIGH
    )

    assert (
        records[1].knowledge_level
        == KnowledgeLevel.TECHNIQUE
    )

    assert (
        records[1].knowledge_domain
        == KnowledgeDomain.SCENE
    )

    assert (
        records[1].importance
        == Importance.MEDIUM
    )

    print(
        "KnowledgeParser tests passed."
    )


if __name__ == "__main__":
    main()