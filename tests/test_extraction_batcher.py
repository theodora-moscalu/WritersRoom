from writersroom.extraction.extraction_batcher import (
    ExtractionBatcher,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():

    print(
        "Testing ExtractionBatcher..."
    )

    units = [
        SourceUnit(
            sequence=i,
            text=f"Scene {i}",
            unit_type=(
                SourceUnitType.SCENE
            ),
        )
        for i in range(
            1,
            11,
        )
    ]

    batcher = (
        ExtractionBatcher()
    )

    batches = (
        batcher.create_batches(
            units,
            batch_size=3,
        )
    )

    assert (
        len(batches)
        == 4
    )

    assert (
        len(batches[0])
        == 3
    )

    assert (
        len(batches[1])
        == 3
    )

    assert (
        len(batches[2])
        == 3
    )

    assert (
        len(batches[3])
        == 1
    )

    print()

    print(
        "ExtractionBatcher tests passed."
    )


if __name__ == "__main__":
    main()