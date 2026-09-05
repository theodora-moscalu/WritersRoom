import json
from pathlib import Path

from writersroom.domains.story.project import Project


class Workspace:
    """Represents the root of a WritersRoom workspace."""

    WORKSPACE_DIRECTORY = Path("workspace")
    WORKSPACE_FILE = (
        WORKSPACE_DIRECTORY / "workspace.json"
    )

    def __init__(self):
        self.projects = []

    def to_dict(self):
        """Convert the workspace to a dictionary."""

        return {
            "projects": self.projects,
        }

    def save(self):
        """Save the workspace."""

        self.WORKSPACE_DIRECTORY.mkdir(
            exist_ok=True
        )

        with open(
            self.WORKSPACE_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.to_dict(),
                file,
                indent=4,
            )

    @classmethod
    def load(cls):
        """Load the workspace."""

        workspace = cls()

        if not cls.WORKSPACE_FILE.exists():
            return workspace

        with open(
            cls.WORKSPACE_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        workspace.projects = data.get(
            "projects",
            [],
        )

        return workspace

    #
    # Project methods
    #

    def add_project(
        self,
        project: Project,
    ):
        """Register a project."""

        if project.title not in self.projects:
            self.projects.append(
                project.title
            )

    def remove_project(
        self,
        title: str,
    ):
        """Remove a project."""

        if title in self.projects:
            self.projects.remove(title)
