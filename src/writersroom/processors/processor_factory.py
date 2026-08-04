from writersroom.importers.document_import_result import (
    DocumentImportResult,
)
from writersroom.processors.base_processor import (
    BaseProcessor,
)
from writersroom.processors.paragraph_processor import (
    ParagraphProcessor,
)
from writersroom.processors.processor_classifier import (
    ProcessorClassifier,
)
from writersroom.processors.processor_type import (
    ProcessorType,
)
from writersroom.processors.scene_processor import (
    SceneProcessor,
)


class ProcessorFactory:
    """Creates document processors."""

    @classmethod
    def create(
        cls,
        imported: DocumentImportResult,
    ) -> BaseProcessor:
        """Create a processor for an imported document."""

        processor_type = (
            ProcessorClassifier.classify(
                imported.text
            )
        )

        if (
            processor_type
            == ProcessorType.SCENE
        ):
            return SceneProcessor()

        if (
            processor_type
            == ProcessorType.PARAGRAPH
        ):
            return ParagraphProcessor()

        raise ValueError(
            f"No processor exists for '{processor_type}'."
        )