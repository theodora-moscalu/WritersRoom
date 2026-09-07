from pathlib import Path

from writersroom.draft.base_reader import DraftReader
from writersroom.draft.fountain_reader import FountainReader
from writersroom.draft.kitscenarist_reader import KitScenaristReader


class DraftReaderFactory:
    """Creates a DraftReader for a script file."""

    _readers = (
        FountainReader,
        KitScenaristReader,
    )

    @classmethod
    def create(cls, path: str) -> DraftReader:
        """Return a reader for `path`, or raise if the format is unsupported."""

        extension = Path(path).suffix.lower()

        for reader_class in cls._readers:
            if extension in reader_class.extensions:
                return reader_class()

        raise ValueError(
            f"No script reader for '{extension}'. "
            "Link a .kitsp or .fountain file."
        )
