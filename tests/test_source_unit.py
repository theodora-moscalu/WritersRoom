from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():
    print("Testing SourceUnit...")

    unit = SourceUnit(
        sequence=1,
        heading="INT. HOUSE - DAY",
        text=(
            "John enters the room."
        ),
        unit_type=SourceUnitType.SCENE,
    )

    assert (
        unit.sequence
        == 1
    )

    assert (
        unit.heading
        == "INT. HOUSE - DAY"
    )

    assert (
        unit.text
        == "John enters the room."
    )

    assert (
        unit.unit_type
        == SourceUnitType.SCENE
    )

    print(
        "SourceUnit tests passed."
    )


if __name__ == "__main__":
    main()