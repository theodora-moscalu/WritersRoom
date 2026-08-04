from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():
    print(
        "Testing ProcessedDocument..."
    )

    document = ProcessedDocument(
        passages=[
            SourceUnit(
                sequence=1,
                text="INT. HOUSE - DAY",
                unit_type=(
                    SourceUnitType.SCENE
                ),
            )
        ],
        metadata={
            "processor": "scene",
        },
    )

    assert (
        len(document.passages)
        == 1
    )

    unit = document.passages[0]

    assert (
        unit.sequence
        == 1
    )

    assert (
        unit.text
        == "INT. HOUSE - DAY"
    )

    assert (
        unit.unit_type
        == SourceUnitType.SCENE
    )

    assert (
        document.metadata["processor"]
        == "scene"
    )

    print(
        "ProcessedDocument tests passed."
    )


if __name__ == "__main__":
    main()