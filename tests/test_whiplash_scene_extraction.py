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
    """Extraction unit used for scene testing."""

    def __init__(
        self,
        text: str,
        heading: str | None = None,
    ):
        self._text = text
        self._heading = heading

    @property
    def text(
        self,
    ) -> str:
        return self._text

    @property
    def heading(
        self,
    ) -> str | None:
        return self._heading


def main():

    print(
        "Whiplash Scene Extraction"
    )

    scene = (
        Path(__file__).parent
        / "data"
        / "whiplash_scene.txt"
    ).read_text(
        encoding="utf-8"
    )

    librarian = (
        KnowledgeLibrarian()
    )

    records = (
        librarian.analyse(
            TestExtractionUnit(
                text=scene,
                heading="Whiplash Scene"
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
        print("=" * 60)
        print(f"Record {index}")
        print("=" * 60)

        print(
            f"Level      : {record.knowledge_level.name}"
        )

        print(
            f"Domain     : {record.knowledge_domain.name}"
        )

        print(
            f"Importance : {record.importance.name}"
        )

        print()

        print("TEXT")

        print(record.text)

        print()

        print("EXPLANATION")

        print(record.explanation)


if __name__ == "__main__":
    main()