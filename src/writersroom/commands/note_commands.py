from writersroom.common.multiline_input import multiline_input
from writersroom.common.selection_menu import (
    choose_from_list,
)


class NoteCommands:
    """Handles note commands."""

    def __init__(self, service):
        self.service = service

    def handle(self, args: list[str]):
        """Handle note commands."""

        if not args:
            self.print_help()
            return

        action = args[0].lower()

        if action == "add":
            self.add(args[1:])
            return

        if action == "list":
            self.list()
            return

        if action == "show":
            self.show(args[1:])
            return

        self.print_help()

    def add(self, args: list[str]):
        """Create a note."""

        if not args:
            print(
                "\nUsage: note add <project|character|episode|location|scene|relationship>\n"
            )
            return

        target = args[0].lower()

        if target == "project":
            self.add_project()
            return

        if target == "character":
            self.add_character()
            return

        if target == "episode":
            self.add_episode()
            return

        if target == "location":
            self.add_location()
            return

        if target == "scene":
            self.add_scene()
            return

        if target == "relationship":
            self.add_relationship()
            return

        print(
            "\nSupported targets: project, character, episode, location, scene, relationship\n"
        )

    def _prompt_for_note(self):
        """Prompt for a note title and content."""

        title = input(
            "\nNote title:\n> "
        ).strip()

        if not title:
            print("\nA title is required.\n")
            return None

        content = multiline_input(
            "Enter note."
        )

        return title, content

    def add_project(self):
        """Create a project note."""

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_project_note(
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def add_character(self):
        """Create a character note."""

        characters = self.service.project.characters

        if not characters:
            print("\nNo characters exist.\n")
            return

        character = choose_from_list(
            title="Choose a character:",
            items=characters,
            display=lambda c: c.name,
        )

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_character_note(
            character.name,
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def add_episode(self):
        """Create an episode note."""

        episodes = self.service.project.episodes

        if not episodes:
            print("\nNo episodes exist.\n")
            return

        episode = choose_from_list(
            title="Choose an episode:",
            items=episodes,
            display=lambda e: e.title,
        )

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_episode_note(
            episode.title,
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def add_location(self):
        """Create a location note."""

        locations = self.service.project.locations

        if not locations:
            print("\nNo locations exist.\n")
            return

        location = choose_from_list(
            title="Choose a location:",
            items=locations,
            display=lambda l: l.name,
        )

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_location_note(
            location.name,
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def add_scene(self):
        """Create a scene note."""

        episodes = self.service.project.episodes

        if not episodes:
            print("\nNo episodes exist.\n")
            return

        episode = choose_from_list(
            title="Choose an episode:",
            items=episodes,
            display=lambda e: e.title,
        )

        if not episode.scenes:
            print("\nThat episode has no scenes.\n")
            return

        scene = choose_from_list(
            title="Choose a scene:",
            items=episode.scenes,
            display=str,
        )

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_scene_note(
            episode.title,
            scene.number,
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def add_relationship(self):
        """Create a relationship note."""

        relationships = (
            self.service.project.character_relationships
        )

        if not relationships:
            print("\nNo relationships exist.\n")
            return

        relationship = choose_from_list(
            title="Choose a relationship:",
            items=relationships,
            display=str,
        )

        note = self._prompt_for_note()

        if note is None:
            return

        title, content = note

        result = self.service.add_relationship_note(
            relationship,
            title,
            content,
        )

        print(f"\n{result.message}\n")

    def list(self):
        """Display all notes."""

        result = self.service.list_notes()

        notes = result.data

        print()

        if not notes:
            print("No notes.")
            print()
            return

        print("Notes")
        print("-----")

        for note in notes:
            print(
                f"- {note.title} "
                f"({note.target_type.value}: "
                f"{note.target_id})"
            )

        print()

    def show(self, args: list[str]):
        """Display a note."""

        if not args:
            print(
                "\nUsage: note show <title>\n"
            )
            return

        title = " ".join(args)

        result = self.service.show_note(title)

        if not result.success:
            print(f"\n{result.message}\n")
            return

        note = result.data

        print()
        print(note.title)
        print("-" * len(note.title))
        print()
        print(f"Target: {note.target_type.value}")
        print(f"Entity: {note.target_id}")
        print()
        print(note.content)
        print()

    def print_help(self):
        """Display note commands."""

        print()
        print("Note commands")
        print("-------------")
        print("note add project")
        print("note add character")
        print("note add episode")
        print("note add location")
        print("note add scene")
        print("note add relationship")
        print("note list")
        print("note show <title>")
        print()