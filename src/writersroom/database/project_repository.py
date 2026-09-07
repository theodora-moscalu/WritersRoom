import json
from datetime import datetime

from writersroom.database.identity_generator import (
    IdentityGenerator,
)
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.story.project import (
    Project,
)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class ProjectRepository:
    """Stores each project (series / workspace) as a JSON blob row."""

    def __init__(self, database):
        self.database = database
        self.identities = IdentityGenerator(database)

    def create(self, title: str) -> Project:
        """Create and persist a new project."""

        identity = self.identities.next(
            IdentityPrefix.PROJECT
        )

        timestamp = _now()

        project = Project(
            title=title,
            identity=identity,
            created=timestamp,
            updated=timestamp,
        )

        self.database.execute(
            "INSERT INTO projects "
            "(identity, title, data, created, updated) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                identity,
                title,
                json.dumps(project.to_dict()),
                timestamp,
                timestamp,
            ),
        )

        return project

    def save(self, project: Project):
        """Persist the current state of a project."""

        project.updated = _now()

        self.database.execute(
            "UPDATE projects "
            "SET title = ?, data = ?, updated = ? "
            "WHERE identity = ?",
            (
                project.title,
                json.dumps(project.to_dict()),
                project.updated,
                project.identity,
            ),
        )

    def get(self, identity: str) -> Project | None:
        """Return a project by identity."""

        row = self.database.query_one(
            "SELECT * FROM projects WHERE identity = ?",
            (identity,),
        )

        return self._from_row(row) if row else None

    def get_by_title(self, title: str) -> Project | None:
        """Return a project by title (case-insensitive)."""

        row = self.database.query_one(
            "SELECT * FROM projects WHERE lower(title) = lower(?)",
            (title,),
        )

        return self._from_row(row) if row else None

    def list(self) -> list[tuple[str, str]]:
        """Return every project as (identity, title), most recently used first."""

        return [
            (row["identity"], row["title"])
            for row in self.database.query(
                "SELECT identity, title FROM projects "
                "ORDER BY updated DESC, title ASC"
            )
        ]

    def rename(self, identity: str, new_title: str):
        """Rename a project."""

        self.database.execute(
            "UPDATE projects SET title = ?, updated = ? "
            "WHERE identity = ?",
            (new_title, _now(), identity),
        )

    def delete(self, identity: str):
        """Delete a project and its general-tier knowledge."""

        self.database.execute(
            "DELETE FROM projects WHERE identity = ?",
            (identity,),
        )

    def _from_row(self, row) -> Project:
        project = Project.from_dict(
            json.loads(row["data"]),
            identity=row["identity"],
            created=row["created"],
            updated=row["updated"],
        )

        # The column is authoritative for the title (rename updates it directly).
        project.title = row["title"]

        return project
