from writersroom.agents.knowledge_librarian import (
    KnowledgeLibrarian,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():

    print(
        "Testing Knowledge Librarian..."
    )

    librarian = (
        KnowledgeLibrarian()
    )

    unit = SourceUnit(
        sequence=1,
        heading="INT. HOUSE - DAY",
        text=(
            "John quietly enters the room. "
            "He notices a photograph on the wall "
            "and immediately leaves."
        ),
        unit_type=(
            SourceUnitType.SCENE
        ),
    )

    records = (
        librarian.analyse(
            unit
        )
    )

    print()

    print(
        f"Extracted {len(records)} records"
    )

    print()

    for index, record in enumerate(
        records,
        start=1,
    ):

        print(
            "-" * 60
        )

        print(
            f"Record {index}"
        )

        print()

        print(
            f"Level: {record.knowledge_level}"
        )

        print(
            f"Domain: {record.knowledge_domain}"
        )

        print(
            f"Importance: {record.importance}"
        )

        print()

        print(record.text)

        print()

        print(record.explanation)

        print()

    assert len(records) > 0

    print(
        "Knowledge Librarian tests passed."
    )


if __name__ == "__main__":
    main()