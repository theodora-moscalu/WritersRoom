from writersroom.extraction.extraction_granularity import (
    ExtractionGranularity,
)
from writersroom.extraction.extraction_unit_selector import (
    ExtractionUnitSelector,
)
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
        "Testing ExtractionUnitSelector..."
    )

    document = ProcessedDocument(
        source_units=[
            SourceUnit(
                sequence=1,
                heading="INT. CLUB",
                text="Andrew enters.",
                unit_type=SourceUnitType.SCENE,
            ),
            SourceUnit(
                sequence=2,
                text="He plays.",
                unit_type=SourceUnitType.PARAGRAPH,
            ),
        ]
    )

    selector = (
        ExtractionUnitSelector()
    )

    source_units = (
        selector.select(
            document,
            ExtractionGranularity.SOURCE_UNIT,
        )
    )

    assert (
        len(source_units)
        == 2
    )

    scenes = (
        selector.select(
            document,
            ExtractionGranularity.SCENE,
        )
    )

    assert (
        len(scenes)
        == 1
    )

    assert (
        scenes[0].heading
        == "INT. CLUB"
    )

    print()

    print(
        "ExtractionUnitSelector tests passed."
    )


if __name__ == "__main__":
    main()