import os
from datetime import datetime

from writersroom.draft.draft import Draft
from writersroom.draft.reader_factory import DraftReaderFactory


class DraftService:
    """Reads the linked script, re-parsing only when the file changes."""

    def __init__(self):
        self._cache: dict[str, tuple[tuple, Draft]] = {}

    def current(self, path: str | None) -> Draft | None:
        """Return the current Draft for a linked path, or None."""

        if not path:
            return None

        try:
            stat = os.stat(path)
        except OSError:
            return None

        signature = (stat.st_mtime_ns, stat.st_size)

        cached = self._cache.get(path)

        if cached is not None and cached[0] == signature:
            return cached[1]

        try:
            reader = DraftReaderFactory.create(path)
            draft = reader.read(path)
        except (ValueError, OSError):
            return None

        draft.read_at = datetime.now().isoformat(timespec="seconds")

        self._cache[path] = (signature, draft)

        return draft
