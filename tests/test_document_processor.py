from writersroom.processors.paragraph_processor import (
    ParagraphProcessor,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():
    print("Testing ParagraphProcessor...")

    processor = ParagraphProcessor()

    text = """
First passage.
Still first passage.

Second passage.

Third passage.
""".strip()

    result = processor.process(
        text
    )

    assert (
        len(result.passages)
        == 3
    )

    first = result.passages[0]

    assert (
        first.sequence
        == 1
    )

    assert (
        first.text
        == (
            "First passage.\n"
            "Still first passage."
        )
    )

    assert (
        first.unit_type
        == SourceUnitType.PARAGRAPH
    )

    second = result.passages[1]

    assert (
        second.sequence
        == 2
    )

    assert (
        second.text
        == "Second passage."
    )

    third = result.passages[2]

    assert (
        third.sequence
        == 3
    )

    assert (
        third.text
        == "Third passage."
    )

    assert (
        result.metadata["processor"]
        == "paragraph"
    )

    print(
        "ParagraphProcessor tests passed."
    )


if __name__ == "__main__":
    main()