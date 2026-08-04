from pathlib import Path

from writersroom.importers.markdown_importer import (
    MarkdownImporter,
)


def main():
    print("Testing MarkdownImporter...")

    test_file = Path(
        "tests/story.md"
    )

    test_file.write_text(
        "# Story\n\nThis is markdown.",
        encoding="utf-8",
    )

    importer = MarkdownImporter()

    result = importer.import_document(
        str(test_file)
    )

    assert (
        result.filename
        == "story.md"
    )

    assert (
        result.metadata["format"]
        == "markdown"
    )

    assert (
        "# Story"
        in result.text
    )

    test_file.unlink()

    print(
        "MarkdownImporter tests passed."
    )


if __name__ == "__main__":
    main()