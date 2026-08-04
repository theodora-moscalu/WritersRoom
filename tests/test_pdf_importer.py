from pathlib import Path

from writersroom.importers.pdf_importer import (
    PdfImporter,
)


def main():
    print("Testing PdfImporter...")

    pdf = Path(
        "tests/data/Whiplash.pdf"
    )

    assert pdf.exists()

    importer = PdfImporter()

    result = importer.import_document(
        str(pdf)
    )

    assert (
        result.filename
        == pdf.name
    )

    assert (
        len(result.text)
        > 0
    )

    print()
    print("First 1000 characters:")
    print("----------------------")
    print(result.text[:1000])
    print()

    print(
        "PdfImporter tests passed."
    )


if __name__ == "__main__":
    main()