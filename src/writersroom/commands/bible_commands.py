from pathlib import Path

from writersroom.review.review_decision import (
    ReviewDecision,
)


class BibleCommands:
    """Handles `bible` commands — importing a series bible document."""

    def __init__(self, service, project):
        self.service = service
        self.project = project

    def handle(self, args: list[str]):
        """Handle bible commands."""

        if not args or args[0].lower() != "import":
            self.print_help()
            return

        if len(args) < 2:
            print("\nUsage: bible import <path to .pptx / .docx / .pdf>\n")
            return

        self.import_bible(" ".join(args[1:]).strip('"'))

    def import_bible(self, path: str):
        """Extract, review and apply a series bible."""

        if not Path(path).exists():
            print(f"\nFile not found: {path}\n")
            return

        print("\nReading the bible...\n")

        try:
            review = self.service.extract(path, self.project)
        except Exception as error:
            print(f"\nCould not read the bible: {error}\n")
            return

        for warning in review.warnings:
            print(f"  ! {warning}")

        if not review.items:
            print("\nNothing to import from this document.\n")
            return

        print(
            f"Found {len(review.items)} entities. "
            "For each: [k]eep or [s]kip (Enter = keep).\n"
        )

        for item in review.items:

            answer = input(f"  {item.label()}  [K/s] ").strip().lower()

            if answer in ("s", "skip", "n", "no"):
                item.decision = ReviewDecision.REJECT

        result = self.service.apply(self.project, review)

        print(f"\n{result.message}\n")

    def print_help(self):
        print()
        print("Bible commands")
        print("--------------")
        print("bible import <path>   Import a series bible (.pptx, .docx, .pdf)")
        print()
