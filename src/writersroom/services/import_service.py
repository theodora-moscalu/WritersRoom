from pathlib import Path

from writersroom.common.result import Result
from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.passage_service import (
    PassageService,
)


class ImportService:
    """Imports documents into the knowledge library."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

        self.document_service = (
            DocumentService(
                workspace
            )
        )

        self.passage_service = (
            PassageService(
                workspace
            )
        )

    def import_document(
        self,
        knowledge_source_name: str,
        path: str,
    ) -> Result:
        """Import a document."""

        importer = (
            ImporterFactory.create(
                path
            )
        )

        imported = (
            importer.import_document(
                path
            )
        )

        processor = (
            ProcessorFactory.create(
                imported
            )
        )

        document_name = (
            Path(path).stem
        )

        result = (
            self.document_service.add_document(
                knowledge_source_name=knowledge_source_name,
                name=document_name,
                description=imported.filename,
            )
        )

        if not result.success:
            return result

        document = result.data

        processed = (
            processor.process(
                imported.text
            )
        )

        for passage in (
            processed.passages
        ):

            self.passage_service.add_passage(
                knowledge_source_name,
                document.name,
                passage.text,
            )

        return Result.ok(
            f"Imported '{document_name}'.",
            data=document,
        )