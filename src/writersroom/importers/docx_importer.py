from pathlib import Path

from docx import Document

from writersroom.importers.base_importer import (
    BaseImporter,
)
from writersroom.importers.document_import_result import (
    DocumentImportResult,
)


class DocxImporter(BaseImporter):
    """Imports Microsoft Word documents."""

    extensions = (
        ".docx",
    )

    def import_document(
        self,
        path: str,
    ) -> DocumentImportResult:

        file = Path(path)

        document = Document(
            str(file)
        )

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        text = "\n\n".join(
            paragraphs
        )

        return DocumentImportResult(
            filename=file.name,
            text=text,
            metadata={
                "format": "docx",
            },
        )