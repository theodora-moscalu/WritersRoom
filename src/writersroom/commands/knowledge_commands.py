from writersroom.common.selection_menu import (
    choose_from_list,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)


class KnowledgeCommands:
    """Handles knowledge source commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle knowledge commands."""

        if not args:
            self.print_help()
            return

        action = args[0].lower()

        if action == "add":
            self.add()
            return

        if action == "list":
            self.list()
            return

        if action == "show":
            self.show(args[1:])
            return

        if action == "delete":
            self.delete(args[1:])
            return

        self.print_help()

    def add(self):
        """Create a knowledge source."""

        name = input(
            "\nKnowledge source name:\n> "
        ).strip()

        if not name:
            print("\nA name is required.\n")
            return

        source_type = choose_from_list(
            title="Choose a source type:",
            items=list(KnowledgeSourceType),
            display=lambda t: t.value,
        )

        author = input(
            "\nAuthor (optional):\n> "
        ).strip()

        description = input(
            "\nDescription (optional):\n> "
        ).strip()

        result = self.service.add_source(
            name=name,
            source_type=source_type,
            author=author,
            description=description,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display all knowledge sources."""

        result = self.service.list_sources()

        sources = result.data

        print()

        if not sources:
            print("No knowledge sources.")
            print()
            return

        print("Knowledge Sources")
        print("-----------------")

        for source in sources:
            print(
                f"- {source.name} "
                f"({source.source_type.value})"
            )

        print()

    def show(self, args: list[str]):
        """Display a knowledge source."""

        if not args:
            print(
                "\nUsage: knowledge show <name>\n"
            )
            return

        name = " ".join(args)

        result = self.service.show_source(name)

        if not result.success:
            print(f"\n{result.message}\n")
            return

        source = result.data

        print()
        print(source.name)
        print("-" * len(source.name))
        print()
        print(f"Identity: {source.identity}")
        print(f"Type: {source.source_type.value}")
        print(f"Author: {source.author}")

        if source.description:
            print(
                f"Description: {source.description}"
            )

        print(
            f"Documents: {len(source.documents)}"
        )

        print()

    def delete(self, args: list[str]):
        """Delete a knowledge source."""

        if not args:
            print(
                "\nUsage: knowledge delete <name>\n"
            )
            return

        name = " ".join(args)

        result = self.service.delete_source(
            name
        )

        print(f"\n{result.message}\n")

    def print_help(self):
        """Display knowledge commands."""

        print()
        print("Knowledge commands")
        print("------------------")
        print("knowledge add")
        print("knowledge list")
        print("knowledge show <name>")
        print("knowledge delete <name>")
        print()