from pathlib import Path

from writersroom.importers.base_importer import (
    BaseImporter,
)
from writersroom.importers.document_import_result import (
    DocumentImportResult,
)


class TextImporter(BaseImporter):
    """Imports plain text documents."""

    extensions = (
        ".txt",
    )

    def import_document(
        self,
        path: str,
    ) -> DocumentImportResult:

        file = Path(path)

        text = file.read_text(
            encoding="utf-8",
        )

        return DocumentImportResult(
            filename=file.name,
            text=text,
        )