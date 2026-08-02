import json
from pathlib import Path

from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.knowledge.knowledge_library import (
    KnowledgeLibrary,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.domains.story.project import Project


class Workspace:
    """Represents the root of a WritersRoom workspace."""

    WORKSPACE_DIRECTORY = Path("workspace")
    WORKSPACE_FILE = (
        WORKSPACE_DIRECTORY / "workspace.json"
    )

    def __init__(self):
        self.projects = []
        self.knowledge_library = (
            KnowledgeLibrary()
        )
        self.personal_knowledge = []
        self.identity_counters = {}

    def to_dict(self):
        """Convert the workspace to a dictionary."""

        return {
            "projects": self.projects,
            "knowledge_library": (
                self.knowledge_library.to_dict()
            ),
            "personal_knowledge": (
                self.personal_knowledge
            ),
            "identity_counters": (
                self.identity_counters
            ),
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

        if not cls.WORKSPACE_FILE.exists():
            return cls()

        with open(
            cls.WORKSPACE_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        workspace = cls()

        workspace.projects = data.get(
            "projects",
            [],
        )

        workspace.knowledge_library = (
            KnowledgeLibrary.from_dict(
                data.get(
                    "knowledge_library",
                    {},
                )
            )
        )

        workspace.personal_knowledge = (
            data.get(
                "personal_knowledge",
                [],
            )
        )

        workspace.identity_counters = (
            data.get(
                "identity_counters",
                {},
            )
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

    #
    # Knowledge source methods
    #

    def add_knowledge_source(
        self,
        knowledge_source: KnowledgeSource,
    ):
        """Add a knowledge source."""

        self.knowledge_library.add_source(
            knowledge_source
        )

    def find_knowledge_source(
        self,
        identity: str,
    ):
        """Find a knowledge source by identity."""

        return (
            self.knowledge_library.find_source(
                identity
            )
        )

    def find_knowledge_source_by_name(
        self,
        name: str,
    ):
        """Find a knowledge source by name."""

        return (
            self.knowledge_library.find_source_by_name(
                name
            )
        )

    def remove_knowledge_source(
        self,
        identity: str,
    ):
        """Remove a knowledge source."""

        self.knowledge_library.remove_source(
            identity
        )

    def list_knowledge_sources(
        self,
    ):
        """Return all knowledge sources."""

        return (
            self.knowledge_library.knowledge_sources
        )

    #
    # Identity methods
    #

    def generate_identity(
        self,
        prefix: IdentityPrefix,
    ) -> str:
        """Generate the next identity."""

        key = prefix.value

        current = (
            self.identity_counters.get(
                key,
                0,
            )
        )

        current += 1

        self.identity_counters[key] = current

        return (
            f"{key}"
            f"{current:06d}"
        )