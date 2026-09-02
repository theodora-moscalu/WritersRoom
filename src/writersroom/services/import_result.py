from dataclasses import dataclass

from writersroom.domains.knowledge.document import (
    Document,
)
from writersroom.processors.processed_document import (
    ProcessedDocument,
)


@dataclass
class ImportResult:
    """Contains the results of importing a document."""

    document: Document
    processed_document: ProcessedDocument