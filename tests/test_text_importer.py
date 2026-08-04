from pathlib import Path

from writersroom.importers.text_importer import (
    TextImporter,
)


def main():
    print("Testing TextImporter...")

    test_file = Path(
        "tests/test_document.txt"
    )

    test_file.write_text(
        "Hello WritersRoom!",
        encoding="utf-8",
    )

    importer = TextImporter()

    result = importer.import_document(
        str(test_file)
    )

    assert (
        result.filename
        == "test_document.txt"
    )

    assert (
        result.text
        == "Hello WritersRoom!"
    )

    assert result.metadata == {}

    test_file.unlink()

    print(
        "TextImporter tests passed."
    )


if __name__ == "__main__":
    main()