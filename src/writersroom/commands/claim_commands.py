from writersroom.common.multiline_input import (
    multiline_input,
)
from writersroom.common.selection_menu import (
    choose_from_list,
)


class ClaimCommands:
    """Handles claim commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle claim commands."""

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
        """Prompt for a knowledge source."""

        sources = (
            self.service.workspace
            .list_knowledge_sources()
        )

        if not sources:
            print("\nNo knowledge sources exist.\n")
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
        """Prompt for a document."""

        documents = (
            knowledge_source.list_documents()
        )

        if not documents:
            print("\nNo documents exist.\n")
            return None

        return choose_from_list(
            title="Choose a document:",
            items=documents,
            display=lambda d: d.name,
        )

    def _choose_passage(
        self,
        document,
    ):
        """Prompt for a passage."""

        passages = (
            document.list_passages()
        )

        if not passages:
            print("\nNo passages exist.\n")
            return None

        return choose_from_list(
            title="Choose a passage:",
            items=passages,
            display=lambda p: (
                f"{p.sequence}. "
                f"{p.text[:60]}"
            ),
        )

    def add(self):
        """Create a claim."""

        source = self._choose_knowledge_source()

        if source is None:
            return

        document = self._choose_document(
            source
        )

        if document is None:
            return

        passage = self._choose_passage(
            document
        )

        if passage is None:
            return

        print()

        text = input(
            "Claim:\n> "
        ).strip()

        explanation = multiline_input(
            "Explanation."
        )

        result = self.service.add_claim(
            source.name,
            document.name,
            passage.sequence,
            text,
            explanation,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display claims."""

        source = self._choose_knowledge_source()

        if source is None:
            return

        document = self._choose_document(
            source
        )

        if document is None:
            return

        passage = self._choose_passage(
            document
        )

        if passage is None:
            return

        result = self.service.list_claims(
            source.name,
            document.name,
            passage.sequence,
        )

        print()

        if not result.data:
            print("No claims.")
            print()
            return

        print("Claims")
        print("------")

        for claim in result.data:
            print(
                f"{claim.identity}: "
                f"{claim.text}"
            )

        print()

    def show(self):
        """Display a claim."""

        source = self._choose_knowledge_source()

        if source is None:
            return

        document = self._choose_document(
            source
        )

        if document is None:
            return

        passage = self._choose_passage(
            document
        )

        if passage is None:
            return

        claims = passage.list_claims()

        if not claims:
            print("\nNo claims.\n")
            return

        claim = choose_from_list(
            title="Choose a claim:",
            items=claims,
            display=lambda c: c.text,
        )

        result = self.service.show_claim(
            source.name,
            document.name,
            passage.sequence,
            claim.identity,
        )

        if not result.success:
            print(f"\n{result.message}\n")
            return

        claim = result.data

        print()
        print(claim.identity)
        print("-" * len(claim.identity))
        print()
        print(claim.text)

        if claim.explanation:
            print()
            print("Explanation")
            print("-----------")
            print(claim.explanation)

        print()

    def delete(self):
        """Delete a claim."""

        source = self._choose_knowledge_source()

        if source is None:
            return

        document = self._choose_document(
            source
        )

        if document is None:
            return

        passage = self._choose_passage(
            document
        )

        if passage is None:
            return

        claims = passage.list_claims()

        if not claims:
            print("\nNo claims.\n")
            return

        claim = choose_from_list(
            title="Choose a claim:",
            items=claims,
            display=lambda c: c.text,
        )

        result = self.service.delete_claim(
            source.name,
            document.name,
            passage.sequence,
            claim.identity,
        )

        print(f"\n{result.message}\n")

    def print_help(self):
        """Display claim commands."""

        print()
        print("Claim commands")
        print("--------------")
        print("claim add")
        print("claim list")
        print("claim show")
        print("claim delete")
        print()