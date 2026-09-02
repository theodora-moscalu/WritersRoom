from pathlib import Path

from writersroom.common.result import Result
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)
from writersroom.services.import_result import (
    ImportResult,
)

class ImportService:
    """Imports documents into the knowledge library."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

        self.knowledge_source_service = (
            KnowledgeSourceService(
                workspace
            )
        )

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
        knowledge_source_type: KnowledgeSourceType,
        path: str,
        document_name: str | None = None,
    ) -> Result:
        """Import a document."""

        if (
            self.workspace.find_knowledge_source_by_name(
                knowledge_source_name
            )
            is None
        ):

            result = (
                self.knowledge_source_service.add_source(
                    name=knowledge_source_name,
                    source_type=knowledge_source_type,
                )
            )

            if not result.success:
                return result

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

        if document_name is None:
            document_name = Path(path).stem

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

        for source_unit in (
            processed.source_units
        ):

            self.passage_service.add_passage(
                knowledge_source_name,
                document.name,
                source_unit.text,
            )

        return Result.ok(
            f"Imported '{document_name}'.",
            data=ImportResult(
                document=document,
                processed_document=processed,
            ),
        )