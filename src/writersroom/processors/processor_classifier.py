import re

from writersroom.processors.processor_type import (
    ProcessorType,
)


class ProcessorClassifier:
    """Classifies imported documents."""

    _scene_heading = re.compile(
        r"^(INT\.|EXT\.|INT/EXT\.|I/E\.)",
        re.IGNORECASE | re.MULTILINE,
    )

    @classmethod
    def classify(
        cls,
        text: str,
    ) -> ProcessorType:
        """Determine the most suitable processor."""

        if cls._scene_heading.search(
            text
        ):
            return (
                ProcessorType.SCENE
            )

        return (
            ProcessorType.PARAGRAPH
        )