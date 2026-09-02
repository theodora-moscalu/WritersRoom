from writersroom.processors.scene import (
    Scene,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():

    print(
        "Testing Scene..."
    )

    scene = Scene(
        heading="INT. JAZZ CLUB - NIGHT",
        source_units=[
            SourceUnit(
                sequence=1,
                text="Andrew plays.",
                unit_type=SourceUnitType.SCENE,
            ),
            SourceUnit(
                sequence=2,
                text="Fletcher watches.",
                unit_type=SourceUnitType.PARAGRAPH,
            ),
        ],
    )

    assert (
        scene.first_sequence
        == 1
    )

    assert (
        scene.last_sequence
        == 2
    )

    assert (
        "Andrew plays."
        in scene.text
    )

    assert (
        "Fletcher watches."
        in scene.text
    )

    print()

    print(
        "Scene tests passed."
    )


if __name__ == "__main__":
    main()