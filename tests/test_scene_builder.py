from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.scene_builder import (
    SceneBuilder,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():

    print(
        "Testing SceneBuilder..."
    )

    document = ProcessedDocument(
        source_units=[
            SourceUnit(
                sequence=1,
                heading="INT. JAZZ CLUB - NIGHT",
                text="Andrew enters.",
                unit_type=SourceUnitType.SCENE,
            ),
            SourceUnit(
                sequence=2,
                text="He sits at the drums.",
                unit_type=SourceUnitType.PARAGRAPH,
            ),
            SourceUnit(
                sequence=3,
                heading="INT. PRACTICE ROOM - DAY",
                text="Andrew practises.",
                unit_type=SourceUnitType.SCENE,
            ),
            SourceUnit(
                sequence=4,
                text="Fletcher arrives.",
                unit_type=SourceUnitType.PARAGRAPH,
            ),
        ]
    )

    builder = (
        SceneBuilder()
    )

    scenes = builder.build(
        document
    )

    assert (
        len(scenes)
        == 2
    )

    assert (
        scenes[0].heading
        == "INT. JAZZ CLUB - NIGHT"
    )

    assert (
        scenes[1].heading
        == "INT. PRACTICE ROOM - DAY"
    )

    assert (
        scenes[0].first_sequence
        == 1
    )

    assert (
        scenes[0].last_sequence
        == 2
    )

    assert (
        scenes[1].first_sequence
        == 3
    )

    assert (
        scenes[1].last_sequence
        == 4
    )

    print()

    print(
        "SceneBuilder tests passed."
    )


if __name__ == "__main__":
    main()