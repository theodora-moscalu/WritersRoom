from pathlib import Path

from pypdf import PdfReader

from writersroom.importers.base_importer import (
    BaseImporter,
)
from writersroom.importers.document_import_result import (
    DocumentImportResult,
)


class PdfImporter(BaseImporter):
    """Imports text from digital PDF files."""

    extensions = (
        ".pdf",
    )

    def import_document(
        self,
        path: str,
    ) -> DocumentImportResult:
        """Import a PDF document."""

        reader = PdfReader(path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(
                    text.strip()
                )

        text = "\n\n".join(
            pages
        ).strip()

        if not text:
            raise ValueError(
                "No text could be extracted from the PDF. "
                "The document may be scanned or image-based."
            )

        return DocumentImportResult(
            filename=Path(path).name,
            text=text,
        )