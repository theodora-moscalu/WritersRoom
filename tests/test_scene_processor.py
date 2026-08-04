from writersroom.processors.scene_processor import (
    SceneProcessor,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():
    print(
        "Testing SceneProcessor..."
    )

    screenplay = """
INT. HOUSE - DAY

John enters.

MARY
Hello.

EXT. STREET - NIGHT

Cars rush past.
"""

    processor = (
        SceneProcessor()
    )

    document = (
        processor.process(
            screenplay
        )
    )

    assert (
        len(
            document.source_units
        )
        == 2
    )

    scene = (
        document.source_units[0]
    )

    assert (
        scene.sequence
        == 1
    )

    assert (
        scene.heading
        == "INT. HOUSE - DAY"
    )

    assert (
        scene.unit_type
        == SourceUnitType.SCENE
    )

    assert (
        "John enters."
        in scene.text
    )

    scene = (
        document.source_units[1]
    )

    assert (
        scene.sequence
        == 2
    )

    assert (
        scene.heading
        == "EXT. STREET - NIGHT"
    )

    assert (
        scene.unit_type
        == SourceUnitType.SCENE
    )

    assert (
        "Cars rush past."
        in scene.text
    )

    print(
        "SceneProcessor tests passed."
    )


if __name__ == "__main__":
    main()