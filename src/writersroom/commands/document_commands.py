from writersroom.common.selection_menu import (
    choose_from_list,
)


class DocumentCommands:
    """Handles document commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle document commands."""

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
            self.show()
            return

        if action == "delete":
            self.delete()
            return

        self.print_help()

    def _choose_knowledge_source(self):
        """Prompt the user to choose a knowledge source."""

        sources = (
            self.service.workspace
            .list_knowledge_sources()
        )

        if not sources:
            print(
                "\nNo knowledge sources exist.\n"
            )
            return None

        return choose_from_list(
            title="Choose a knowledge source:",
            items=sources,
            display=lambda s: s.name,
        )

    def add(self):
        """Create a document."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        name = input(
            "\nDocument name:\n> "
        ).strip()

        if not name:
            print("\nA name is required.\n")
            return

        description = input(
            "\nDescription (optional):\n> "
        ).strip()

        result = self.service.add_document(
            knowledge_source.name,
            name,
            description,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display documents."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        result = self.service.list_documents(
            knowledge_source.name
        )

        documents = result.data

        print()

        if not documents:
            print("No documents.")
            print()
            return

        print("Documents")
        print("---------")

        for document in documents:
            print(document.name)

        print()

    def show(self):
        """Display a document."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        name = input(
            "\nDocument name:\n> "
        ).strip()

        result = self.service.show_document(
            knowledge_source.name,
            name,
        )

        if not result.success:
            print(f"\n{result.message}\n")
            return

        document = result.data

        print()
        print(document.name)
        print("-" * len(document.name))
        print()
        print(f"Identity: {document.identity}")
        print(
            f"Description: {document.description}"
        )
        print(
            f"Passages: {len(document.passages)}"
        )
        print()

    def delete(self):
        """Delete a document."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        name = input(
            "\nDocument name:\n> "
        ).strip()

        result = self.service.delete_document(
            knowledge_source.name,
            name,
        )

        print(f"\n{result.message}\n")

    def print_help(self):
        """Display document commands."""

        print()
        print("Document commands")
        print("-----------------")
        print("document add")
        print("document list")
        print("document show")
        print("document delete")
        print()