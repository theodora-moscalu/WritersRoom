from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.importers.text_importer import (
    TextImporter,
)


def main():
    print("Testing ImporterFactory...")

    importer = ImporterFactory.create(
        "story.txt"
    )

    assert isinstance(
        importer,
        TextImporter,
    )

    try:
        ImporterFactory.create(
            "story.xyz"
        )

        assert False

    except ValueError:
        pass

    print(
        "ImporterFactory tests passed."
    )


if __name__ == "__main__":
    main()