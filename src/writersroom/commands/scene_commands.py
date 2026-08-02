from writersroom.common.multiline_input import multiline_input
from writersroom.common.selection_menu import choose_from_list


class SceneCommands:
    """Handles commands related to scenes."""

    def __init__(self, episode_service):
        self.service = episode_service

    def handle(self, args: list[str]):
        """Handle scene commands."""

        if not args:
            self.print_help()
            return

        action = args[0].lower()

        if action == "add":
            self.add(args[1:])
            return

        if action == "heading":
            self.heading(args[1:])
            return

        if action == "summary":
            self.summary(args[1:])
            return

        if action == "character":
            self.character(args[1:])
            return

        if action == "location":
            self.location(args[1:])
            return

        print(f"\nUnknown scene command '{action}'.\n")

    def add(self, args: list[str]):
        """Create a new scene."""

        if not args:
            print("\nPlease provide an episode title.\n")
            return

        title = " ".join(args)

        result = self.service.add_scene(title)

        print(f"\n{result.message}\n")

    def heading(self, args: list[str]):
        """Set a scene heading."""

        if len(args) < 2:
            print(
                "\nUsage: episode scene heading <episode> <scene number>\n"
            )
            return

        try:
            scene_number = int(args[-1])
        except ValueError:
            print("\nScene number must be an integer.\n")
            return

        episode_title = " ".join(args[:-1])

        heading = input("\nEnter scene heading:\n> ").strip()

        result = self.service.set_scene_heading(
            episode_title,
            scene_number,
            heading,
        )

        print(f"\n{result.message}\n")

    def summary(self, args: list[str]):
        """Set a scene summary."""

        if len(args) < 2:
            print(
                "\nUsage: episode scene summary <episode> <scene number>\n"
            )
            return

        try:
            scene_number = int(args[-1])
        except ValueError:
            print("\nScene number must be an integer.\n")
            return

        episode_title = " ".join(args[:-1])

        summary = multiline_input(
            "Enter scene summary."
        )

        result = self.service.set_scene_summary(
            episode_title,
            scene_number,
            summary,
        )

        print(f"\n{result.message}\n")

    def character(self, args: list[str]):
        """Attach a character to a scene."""

        if len(args) < 2:
            print(
                "\nUsage: episode scene character <episode> <scene number>\n"
            )
            return

        try:
            scene_number = int(args[-1])
        except ValueError:
            print("\nScene number must be an integer.\n")
            return

        episode_title = " ".join(args[:-1])

        characters = self.service.project.characters

        if not characters:
            print(
                "\nThere are no characters in this project.\n"
            )
            return

        selected = choose_from_list(
            title="Choose a character:",
            items=characters,
            display=lambda c: c.name,
        )

        result = self.service.add_scene_character(
            episode_title,
            scene_number,
            selected.name,
        )

        print(f"\n{result.message}\n")

    def location(self, args: list[str]):
        """Attach a location to a scene."""

        if len(args) < 2:
            print(
                "\nUsage: episode scene location <episode> <scene number>\n"
            )
            return

        try:
            scene_number = int(args[-1])
        except ValueError:
            print("\nScene number must be an integer.\n")
            return

        episode_title = " ".join(args[:-1])

        locations = self.service.project.locations

        if not locations:
            print(
                "\nThere are no locations in this project.\n"
            )
            return

        selected = choose_from_list(
            title="Choose a location:",
            items=locations,
            display=lambda l: l.name,
        )

        result = self.service.add_scene_location(
            episode_title,
            scene_number,
            selected.name,
        )

        print(f"\n{result.message}\n")

    def print_help(self):
        """Display scene commands."""

        print()
        print("Scene commands")
        print("--------------")
        print("episode scene add <episode>")
        print("episode scene heading <episode> <scene number>")
        print("episode scene summary <episode> <scene number>")
        print("episode scene character <episode> <scene number>")
        print("episode scene location <episode> <scene number>")
        print()