from writersroom.common.multiline_input import (
    multiline_input,
)
from writersroom.common.selection_menu import (
    choose_from_list,
)


class PassageCommands:
    """Handles passage commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle passage commands."""

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

    def _choose_document(
        self,
        knowledge_source,
    ):
        """Prompt the user to choose a document."""

        documents = (
            knowledge_source.list_documents()
        )

        if not documents:
            print(
                "\nNo documents exist.\n"
            )
            return None

        return choose_from_list(
            title="Choose a document:",
            items=documents,
            display=lambda d: d.name,
        )

    def add(self):
        """Create a passage."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        document = self._choose_document(
            knowledge_source
        )

        if document is None:
            return

        text = multiline_input(
            "Enter passage."
        )

        result = self.service.add_passage(
            knowledge_source.name,
            document.name,
            text,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display passages."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        document = self._choose_document(
            knowledge_source
        )

        if document is None:
            return

        result = self.service.list_passages(
            knowledge_source.name,
            document.name,
        )

        print()

        if not result.data:
            print("No passages.")
            print()
            return

        print("Passages")
        print("--------")

        for passage in result.data:
            print(
                f"{passage.sequence}. "
                f"{passage.text[:60]}"
            )

        print()

    def show(self):
        """Display a passage."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        document = self._choose_document(
            knowledge_source
        )

        if document is None:
            return

        sequence = int(
            input(
                "\nPassage number:\n> "
            )
        )

        result = self.service.show_passage(
            knowledge_source.name,
            document.name,
            sequence,
        )

        if not result.success:
            print(f"\n{result.message}\n")
            return

        passage = result.data

        print()
        print(
            f"Passage {passage.sequence}"
        )
        print("----------------")
        print()
        print(passage.text)
        print()

    def delete(self):
        """Delete a passage."""

        knowledge_source = (
            self._choose_knowledge_source()
        )

        if knowledge_source is None:
            return

        document = self._choose_document(
            knowledge_source
        )

        if document is None:
            return

        sequence = int(
            input(
                "\nPassage number:\n> "
            )
        )

        result = self.service.delete_passage(
            knowledge_source.name,
            document.name,
            sequence,
        )

        print(f"\n{result.message}\n")

    def print_help(self):
        """Display passage commands."""

        print()
        print("Passage commands")
        print("----------------")
        print("passage add")
        print("passage list")
        print("passage show")
        print("passage delete")
        print()