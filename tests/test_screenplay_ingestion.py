from pathlib import Path

from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)


def main():
    print(
        "Testing screenplay ingestion..."
    )

    pdf = (
        Path(__file__).parent
        / "data"
        / "Whiplash.pdf"
    )

    importer = (
        ImporterFactory.create(
            str(pdf)
        )
    )

    imported = importer.import_document(
        str(pdf)
    )

    processor = (
        ProcessorFactory.create(
            imported
        )
    )

    document = (
        processor.process(
            imported.text
        )
    )

    print()

    print(
        f"Created {len(document.source_units)} "
        "source units."
    )

    first = (
        document.source_units[0]
    )

    print()

    print(
        "First scene heading:"
    )

    print(first.heading)

    print()

    print(
        "First 400 characters:"
    )

    print(first.text[:400])

    assert (
        len(
            document.source_units
        )
        > 100
    )

    print()

    print(
        "Screenplay ingestion tests passed."
    )


if __name__ == "__main__":
    main()