import json
from pathlib import Path

from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)
from writersroom.database.project_repository import (
    ProjectRepository,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.domains.story.project import (
    Project,
)


class LegacyImport:
    """One-time import of pre-database JSON files."""

    WORKSPACE_FILE = Path("workspace") / "workspace.json"
    PROJECTS_DIRECTORY = Path("projects")

    def __init__(
        self,
        database,
        workspace_file: Path | None = None,
        projects_directory: Path | None = None,
    ):
        self.database = database
        self.workspace_file = workspace_file or self.WORKSPACE_FILE
        self.projects_directory = (
            projects_directory or self.PROJECTS_DIRECTORY
        )
        self.knowledge = KnowledgeRepository(database)
        self.projects = ProjectRepository(database)

    def run_if_needed(self):
        """Import the legacy knowledge library and projects once."""

        self._import_knowledge_library()
        self._import_projects()

    #
    # Knowledge library (workspace.json -> writing tier)
    #

    def _import_knowledge_library(self):
        if self._count("knowledge_sources") > 0:
            return

        if not self.workspace_file.exists():
            return

        data = json.loads(
            self.workspace_file.read_text(encoding="utf-8")
        )

        sources = (
            data.get("knowledge_library", {})
            .get("knowledge_sources", [])
        )

        if not sources:
            return

        for prefix, value in data.get(
            "identity_counters", {}
        ).items():
            self.database.execute(
                "INSERT INTO identity_counters (prefix, value) "
                "VALUES (?, ?) "
                "ON CONFLICT(prefix) DO UPDATE SET value = excluded.value",
                (prefix, value),
            )

        for source_data in sources:

            source = KnowledgeSource.from_dict(source_data)

            self.knowledge.add_source(source, tier="writing")

            for document in source.documents:

                self.knowledge.add_document(document)

                for passage in document.passages:

                    self.knowledge.add_passage(passage)

                    for claim in passage.claims:

                        self.knowledge.add_claim(claim)

    #
    # Projects (projects/*.json -> projects table)
    #

    def _import_projects(self):
        if self._count("projects") > 0:
            return

        if not self.projects_directory.exists():
            return

        for path in sorted(
            self.projects_directory.glob("*.json")
        ):

            data = json.loads(
                path.read_text(encoding="utf-8")
            )

            project = self.projects.create(data["title"])

            loaded = Project.from_dict(
                data,
                identity=project.identity,
            )

            self.projects.save(loaded)

    def _count(self, table: str) -> int:
        row = self.database.query_one(
            f"SELECT COUNT(*) AS total FROM {table}"
        )

        return row["total"]
