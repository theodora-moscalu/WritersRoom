from abc import ABC
from abc import abstractmethod

from writersroom.draft.draft import Draft


class DraftReader(ABC):
    """Reads the current script from an external file into a Draft."""

    extensions: tuple[str, ...] = ()

    @abstractmethod
    def read(self, path: str) -> Draft:
        """Parse the script file at `path`."""

        raise NotImplementedError
