from pathlib import Path

from writersroom.agents.knowledge_librarian import (
    KnowledgeLibrarian,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)


class TestExtractionUnit(
    ExtractionUnit
):
    """Simple extraction unit used by the golden extraction test."""

    def __init__(
        self,
        text: str,
    ):
        self._text = text

    @property
    def text(
        self,
    ) -> str:
        return self._text


def main():

    print(
        "Golden Extraction Test"
    )

    text = (
        Path(__file__).parent
        / "data"
        / "golden_extraction.txt"
    ).read_text(
        encoding="utf-8"
    )

    librarian = (
        KnowledgeLibrarian()
    )

    records = (
        librarian.analyse(
            TestExtractionUnit(
                text
            )
        )
    )

    print()

    print(
        f"Extracted {len(records)} record(s)"
    )

    for index, record in enumerate(
        records,
        start=1,
    ):

        print()

        print(
            "-" * 60
        )

        print(
            f"Record {index}"
        )

        print(
            f"Level: {record.knowledge_level.name}"
        )

        print(
            f"Domain: {record.knowledge_domain.name}"
        )

        print(
            f"Importance: {record.importance.name}"
        )

        print()

        print(record.text)

        print()

        print(record.explanation)


if __name__ == "__main__":
    main()