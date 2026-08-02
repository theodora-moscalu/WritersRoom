from writersroom.common.selection_menu import choose_from_list
from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)


class CharacterRelationshipCommands:
    """Handles character relationship commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle relationship commands."""

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

        self.print_help()

    def add(self):
        """Create a new relationship."""

        characters = self.service.project.characters

        if len(characters) < 2:
            print(
                "\nAt least two characters are required.\n"
            )
            return

        source = choose_from_list(
            title="Choose the source character:",
            items=characters,
            display=lambda c: c.name,
        )

        relationship = choose_from_list(
            title="Choose the relationship:",
            items=list(RelationshipType),
            display=lambda r: r.value,
        )

        available_targets = [
            character
            for character in characters
            if character.name != source.name
        ]

        target = choose_from_list(
            title="Choose the target character:",
            items=available_targets,
            display=lambda c: c.name,
        )

        result = self.service.add_relationship(
            source.name,
            relationship,
            target.name,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display all relationships."""

        relationships = (
            self.service.project.character_relationships
        )

        print()

        if not relationships:
            print("No relationships.")
            print()
            return

        print("Character Relationships")
        print("-----------------------")

        for relationship in relationships:
            print(relationship)

        print()

    def print_help(self):
        """Display relationship commands."""

        print()
        print("Relationship commands")
        print("---------------------")
        print("relationship add")
        print("relationship list")
        print()