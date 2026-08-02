from writersroom.commands.base_entity_commands import BaseEntityCommands
from writersroom.commands.scene_commands import SceneCommands
from writersroom.common.multiline_input import multiline_input
from writersroom.common.selection_menu import choose_from_list


class EpisodeCommands(BaseEntityCommands):
    """Handles all episode-related commands."""

    def __init__(self, service):
        super().__init__("episode", service)

        self.scene_commands = SceneCommands(service)

    @property
    def entity_name(self) -> str:
        return "Episode"

    @property
    def entity_name_plural(self) -> str:
        return "Episodes"

    def handle_custom_command(
        self,
        action: str,
        args: list[str],
    ) -> bool:
        """Handle episode-specific commands."""

        if action == "logline":
            self.set_logline(args)
            return True

        if action == "synopsis":
            self.set_synopsis(args)
            return True

        if action == "character":
            self.add_character(args)
            return True

        if action == "scene":
            self.scene_commands.handle(args)
            return True

        if action == "show":
            self.show(args)
            return True

        return super().handle_custom_command(action, args)

    def print_custom_help(self):
        """Display episode-specific help."""

        print("episode logline <title>")
        print("episode synopsis <title>")
        print("episode character <title>")
        print("episode scene add <title>")
        print("episode show <title>")

    def set_logline(self, args: list[str]):
        if not args:
            print("\nPlease provide an episode title.\n")
            return

        title = " ".join(args)

        logline = input("\nEnter logline:\n> ").strip()

        result = self.service.set_logline(title, logline)

        print(f"\n{result.message}\n")

    def set_synopsis(self, args: list[str]):
        if not args:
            print("\nPlease provide an episode title.\n")
            return

        title = " ".join(args)

        synopsis = multiline_input("Enter synopsis.")

        result = self.service.set_synopsis(
            title,
            synopsis,
        )

        print(f"\n{result.message}\n")

    def add_character(self, args: list[str]):
        """Attach an existing character to an episode."""

        if not args:
            print("\nPlease provide an episode title.\n")
            return

        title = " ".join(args)

        characters = self.service.project.characters

        if not characters:
            print("\nThere are no characters in this project.\n")
            return

        selected = choose_from_list(
            title="Choose a character:",
            items=characters,
            display=lambda c: c.name,
        )

        result = self.service.add_character(
            title,
            selected.name,
        )

        print(f"\n{result.message}\n")

    def show(self, args: list[str]):
        """Display an episode."""

        if not args:
            print("\nPlease provide an episode title.\n")
            return

        title = " ".join(args)

        result = self.service.show(title)

        if not result.success:
            print(f"\n{result.message}\n")
            return

        episode = result.data

        print()
        print("Episode")
        print("-------")
        print(f"Title: {episode.title}")
        print(f"Status: {episode.status}")
        print()

        print("Logline:")
        print(episode.logline or "(Not set)")
        print()

        print("Synopsis:")
        print(episode.synopsis or "(Not set)")
        print()

        print("Characters:")

        if episode.characters:
            for character in episode.characters:
                print(f"- {character}")
        else:
            print("(None)")

        print()

        print("Locations:")

        if episode.locations:
            for location in episode.locations:
                print(f"- {location}")
        else:
            print("(None)")

        print()

        print("Scenes")
        print("------")

        if not episode.scenes:
            print("(None)")
            print()
            return

        for scene in episode.scenes:

            print()

            print(f"Scene {scene.number}")

            if scene.heading:
                print(scene.heading)
            else:
                print("(No heading)")

            print()

            print("Characters:")

            if scene.characters:
                for character in scene.characters:
                    print(f"- {character}")
            else:
                print("(None)")

            print()

            print("Locations:")

            if scene.locations:
                for location in scene.locations:
                    print(f"- {location}")
            else:
                print("(None)")

            print()

            print("Summary:")

            if scene.summary:
                print(scene.summary)
            else:
                print("(No summary)")