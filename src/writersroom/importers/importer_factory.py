from pathlib import Path

from writersroom.importers.base_importer import (
    BaseImporter,
)
from writersroom.importers.docx_importer import (
    DocxImporter,
)
from writersroom.importers.markdown_importer import (
    MarkdownImporter,
)
from writersroom.importers.pdf_importer import (
    PdfImporter,
)
from writersroom.importers.text_importer import (
    TextImporter,
)


class ImporterFactory:
    """Creates document importers."""

    _importer_classes = (
        TextImporter,
        MarkdownImporter,
        DocxImporter,
        PdfImporter,
    )

    @classmethod
    def create(
        cls,
        path: str,
    ) -> BaseImporter:
        """Create an importer for a document."""

        extension = (
            Path(path)
            .suffix
            .lower()
        )

        for importer_class in (
            cls._importer_classes
        ):

            if (
                extension
                in importer_class.extensions
            ):
                return importer_class()

        raise ValueError(
            f"No importer exists for '{extension}'."
        )