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

        if cached is not None:
            draft.changed_scenes = self._changed_scenes(cached[1], draft)

        self._cache[path] = (signature, draft)

        return draft

    def _changed_scenes(self, previous: Draft, current: Draft) -> list[int]:
        """Scene numbers whose heading or body differs from the previous read."""

        before = {
            scene.number: (scene.heading, scene.text)
            for scene in previous.scenes
        }

        return [
            scene.number
            for scene in current.scenes
            if before.get(scene.number) != (scene.heading, scene.text)
        ]
