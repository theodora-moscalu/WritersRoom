from abc import ABC
from abc import abstractmethod

from writersroom.processors.processed_document import (
    ProcessedDocument,
)


class BaseProcessor(ABC):
    """Base class for document processors."""

    @abstractmethod
    def process(
        self,
        text: str,
    ) -> ProcessedDocument:
        """Process imported text."""

        raise NotImplementedError