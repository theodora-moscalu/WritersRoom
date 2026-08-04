from abc import ABC
from abc import abstractmethod

from writersroom.importers.document_import_result import (
    DocumentImportResult,
)


class BaseImporter(ABC):
    """Base class for document importers."""

    extensions: tuple[str, ...] = ()

    @abstractmethod
    def import_document(
        self,
        path: str,
    ) -> DocumentImportResult:
        """Import a document."""

        raise NotImplementedError