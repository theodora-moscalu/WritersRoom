import json
from pathlib import Path

from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)


class WorkspaceJsonImport:
    """One-time import of the knowledge library from workspace.json."""

    DEFAULT_PATH = Path("workspace") / "workspace.json"

    def __init__(self, database, path=None):
        self.database = database
        self.path = path or self.DEFAULT_PATH
        self.repository = KnowledgeRepository(database)

    def run_if_needed(self) -> int:
        """Import the legacy library once. Return the number of sources imported."""

        if self._already_populated():
            return 0

        if not self.path.exists():
            return 0

        data = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        sources = (
            data.get("knowledge_library", {})
            .get("knowledge_sources", [])
        )

        if not sources:
            return 0

        self._seed_identity_counters(
            data.get("identity_counters", {})
        )

        for source_data in sources:
            self._import_source(source_data)

        return len(sources)

    def _already_populated(self) -> bool:
        row = self.database.query_one(
            "SELECT COUNT(*) AS total FROM knowledge_sources"
        )

        return row["total"] > 0

    def _seed_identity_counters(self, counters: dict):
        for prefix, value in counters.items():
            self.database.execute(
                "INSERT INTO identity_counters (prefix, value) "
                "VALUES (?, ?) "
                "ON CONFLICT(prefix) DO UPDATE SET value = excluded.value",
                (prefix, value),
            )

    def _import_source(self, source_data: dict):
        source = KnowledgeSource.from_dict(source_data)

        self.repository.add_source(source)

        for document in source.documents:

            self.repository.add_document(document)

            for passage in document.passages:

                self.repository.add_passage(passage)

                for claim in passage.claims:

                    self.repository.add_claim(claim)
