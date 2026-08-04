from writersroom.importers.document_import_result import (
    DocumentImportResult,
)
from writersroom.processors.paragraph_processor import (
    ParagraphProcessor,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)
from writersroom.processors.scene_processor import (
    SceneProcessor,
)


def main():
    print(
        "Testing ProcessorFactory..."
    )

    screenplay = (
        DocumentImportResult(
            filename="script.pdf",
            text="""
INT. HOUSE - DAY

John enters.
""",
        )
    )

    processor = (
        ProcessorFactory.create(
            screenplay
        )
    )

    assert isinstance(
        processor,
        SceneProcessor,
    )

    prose = (
        DocumentImportResult(
            filename="book.pdf",
            text="""
Chapter One

Once upon a time...
""",
        )
    )

    processor = (
        ProcessorFactory.create(
            prose
        )
    )

    assert isinstance(
        processor,
        ParagraphProcessor,
    )

    print(
        "ProcessorFactory tests passed."
    )


if __name__ == "__main__":
    main()