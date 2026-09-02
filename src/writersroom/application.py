from writersroom.agents.showrunner import Showrunner
from writersroom.commands.character_commands import CharacterCommands
from writersroom.commands.character_relationship_commands import (
    CharacterRelationshipCommands,
)
from writersroom.commands.claim_commands import (
    ClaimCommands,
)
from writersroom.commands.document_commands import (
    DocumentCommands,
)
from writersroom.commands.episode_commands import EpisodeCommands
from writersroom.commands.knowledge_commands import (
    KnowledgeCommands,
)
from writersroom.commands.location_commands import (
    LocationCommands,
)
from writersroom.commands.note_commands import NoteCommands
from writersroom.commands.passage_commands import (
    PassageCommands,
)
from writersroom.commands.router import CommandRouter
from writersroom.domains.story.project import Project
from writersroom.domains.workspace import Workspace
from writersroom.services.character_relationship_service import (
    CharacterRelationshipService,
)
from writersroom.services.character_service import CharacterService
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.episode_service import EpisodeService
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.location_service import (
    LocationService,
)
from writersroom.services.note_service import NoteService
from writersroom.services.passage_service import (
    PassageService,
)

from writersroom.services.import_service import (
    ImportService,
)

from writersroom.retrieval.retrieval_container import (
    RetrievalContainer,
)

from writersroom.services.knowledge_pipeline_service import (
    KnowledgePipelineService,
)


class Application:
    """Main application for WritersRoom."""

    def __init__(self):
        self.workspace = Workspace.load()

        self.project = Project.load("Untitled Project")

        if self.project is None:
            self.project = Project("Untitled Project")

        self.showrunner = Showrunner(self.project)

        self._build_application()

        self.commands = {
            "help": self._print_help,
            "list": self._list_projects,
            "save": self._save_project,
            "delete": self._delete_project,
        }

        self.argument_commands = {
            "new": (
                self._new_project,
                "Please provide a project name.",
            ),
            "open": (
                self._open_project,
                "Please provide a project name.",
            ),
            "rename": (
                self._rename_project,
                "Please provide a new project name.",
            ),
        }

    def run(self):
        """Run the WritersRoom application."""

        print("Welcome to WritersRoom.")
        self._show_current_project()
        print("Type 'help' for a list of commands.\n")

        while True:
            prompt = input("You: ")

            if self.handle_command(prompt):
                continue

            response = self.showrunner.respond(prompt)

            self.project.save()

            print(f"\nShowrunner: {response}\n")

    def handle_command(self, command: str) -> bool:
        """Handle application commands."""

        command = command.strip()

        if command.lower() == "quit":
            raise SystemExit

        if self.router.dispatch(command):
            return True

        action = command.lower()

        if action in self.commands:
            self.commands[action]()
            return True

        parts = command.split(maxsplit=1)

        if not parts:
            return False

        action = parts[0].lower()

        if action in self.argument_commands:

            function, error_message = self.argument_commands[action]

            self._execute_command_with_argument(
                parts,
                function,
                error_message,
            )

            return True

        return False

    def _execute_command_with_argument(
        self,
        parts: list[str],
        action,
        error_message: str,
    ):
        """Execute a command requiring a single argument."""

        if len(parts) < 2:
            print(f"\n{error_message}\n")
            return

        action(parts[1])

    def _build_application(self):
        """Build application services and command handlers."""

        self.character_service = CharacterService(
            self.project
        )

        self.location_service = LocationService(
            self.project
        )

        self.episode_service = EpisodeService(
            self.project
        )

        self.relationship_service = (
            CharacterRelationshipService(
                self.project
            )
        )

        self.note_service = NoteService(
            self.project
        )

        self.knowledge_source_service = (
            KnowledgeSourceService(
                self.workspace
            )
        )

        self.document_service = (
            DocumentService(
                self.workspace
            )
        )

        self.passage_service = (
            PassageService(
                self.workspace
            )
        )

        self.claim_service = (
            ClaimService(
                self.workspace
            )
        )

        self.import_service = (
            ImportService(
                self.workspace
            )
        )

        self.knowledge_pipeline_service = (
            KnowledgePipelineService(
                self.workspace
                )
        )
        
        self.retrieval = (
            RetrievalContainer(
                self.workspace
            )
        )

        self.router = CommandRouter()

        self.router.register(
            "character",
            CharacterCommands(
                self.character_service,
            ),
        )

        self.router.register(
            "location",
            LocationCommands(
                self.location_service,
            ),
        )

        self.router.register(
            "episode",
            EpisodeCommands(
                self.episode_service,
            ),
        )

        self.router.register(
            "relationship",
            CharacterRelationshipCommands(
                self.relationship_service,
            ),
        )

        self.router.register(
            "note",
            NoteCommands(
                self.note_service,
            ),
        )

        self.router.register(
            "knowledge",
            KnowledgeCommands(
                self.knowledge_source_service,
            ),
        )

        self.router.register(
            "document",
            DocumentCommands(
                self.document_service,
            ),
        )

        self.router.register(
            "passage",
            PassageCommands(
                self.passage_service,
            ),
        )

        self.router.register(
            "claim",
            ClaimCommands(
                self.claim_service,
            ),
        )


    def _switch_project(self, project: Project):
        """Switch to a different project."""

        self.project = project
        self.showrunner = Showrunner(project)

        self._build_application()

        self._show_current_project()

    def _print_help(self):
        """Display the available commands."""

        print()
        print("Available commands")
        print("------------------")
        print("help                         Show this help message")
        print("list                         List all projects")
        print("new <name>                   Create a new project")
        print("open <name>                  Open an existing project")
        print("rename <name>                Rename the current project")
        print("delete                       Delete the current project")
        print("save                         Save the current project")
        print("character add <name>         Add a character")
        print("character list               List characters")
        print("location add <name>          Add a location")
        print("location list                List locations")
        print("episode add <title>          Add an episode")
        print("episode list                 List episodes")
        print("relationship add             Add a relationship")
        print("relationship list            List relationships")
        print("note add project             Add a project note")
        print("note list                    List notes")
        print("note show <title>            Show a note")
        print("knowledge add                Add a knowledge source")
        print("knowledge list               List knowledge sources")
        print("knowledge show               Show a knowledge source")
        print("knowledge delete             Delete a knowledge source")
        print("document add                 Add a document")
        print("document list                List documents")
        print("document show                Show a document")
        print("document delete              Delete a document")
        print("passage add                  Add a passage")
        print("passage list                 List passages")
        print("passage show                 Show a passage")
        print("passage delete               Delete a passage")
        print("claim add                    Add a claim")
        print("claim list                   List claims")
        print("claim show                   Show a claim")
        print("claim delete                 Delete a claim")
        print("quit                         Exit WritersRoom")
        print()

    def _list_projects(self):
        """Display all saved projects."""

        projects = Project.list()

        print()

        if not projects:
            print("No projects found.")
        else:
            print("Projects")
            print("--------")

            for project in projects:
                print(project)

        print()

    def _save_project(self):
        """Save the current project."""

        self.project.save()

        print("\nProject saved.\n")

    def _new_project(self, title: str):
        """Create and switch to a new project."""

        project = Project(title)
        project.save()

        self._switch_project(project)

        print(f"\nCreated project '{title}'.\n")

    def _open_project(self, title: str):
        """Open an existing project."""

        project = Project.load(title)

        if project is None:
            print(f"\nProject '{title}' was not found.\n")
            return

        self._switch_project(project)

        print(f"\nOpened project '{title}'.\n")

    def _rename_project(self, new_title: str):
        """Rename the current project."""

        old_title = self.project.title

        self.project.rename(new_title)

        print(
            f"\nRenamed project '{old_title}' to '{new_title}'."
        )

        self._show_current_project()

        print()

    def _delete_project(self):
        """Delete the current project."""

        print()

        confirmation = input(
            f"Are you sure you want to delete '{self.project.title}'? Type 'yes' to confirm: "
        )

        if confirmation.lower() != "yes":
            print("\nDeletion cancelled.\n")
            return

        deleted_title = self.project.title

        self.project.delete()

        project = Project("Untitled Project")
        project.save()

        self._switch_project(project)

        print(f"\nDeleted project '{deleted_title}'.\n")

    def _show_current_project(self):
        """Display the current project."""

        print(
            f"Current project: {self.project.title}"
        )