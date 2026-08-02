import json
from pathlib import Path

from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import CharacterRelationship
from writersroom.domains.story.episode import Episode
from writersroom.domains.story.location import Location
from writersroom.domains.story.note import Note


class Project:
    """Represents a WritersRoom project."""

    PROJECT_DIRECTORY = Path("projects")

    def __init__(self, title: str):
        self.title = title
        self.conversation_history = []
        self.characters = []
        self.character_relationships = []
        self.locations = []
        self.episodes = []
        self.notes = []

    @property
    def filename(self):
        """Return the project's filename."""

        return self.PROJECT_DIRECTORY / f"{self.title}.json"

    def save(self):
        """Save the project."""

        self.PROJECT_DIRECTORY.mkdir(exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "title": self.title,
                    "conversation_history": self.conversation_history,
                    "characters": [
                        character.to_dict()
                        for character in self.characters
                    ],
                    "character_relationships": [
                        relationship.to_dict()
                        for relationship in self.character_relationships
                    ],
                    "locations": [
                        location.to_dict()
                        for location in self.locations
                    ],
                    "episodes": [
                        episode.to_dict()
                        for episode in self.episodes
                    ],
                    "notes": [
                        note.to_dict()
                        for note in self.notes
                    ],
                },
                file,
                indent=4,
            )

    @classmethod
    def load(cls, title: str):
        """Load a project."""

        filename = cls.PROJECT_DIRECTORY / f"{title}.json"

        if not filename.exists():
            return None

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        project = cls(data["title"])

        project.conversation_history = data.get(
            "conversation_history",
            [],
        )

        project.characters = [
            Character.from_dict(character)
            for character in data.get("characters", [])
        ]

        project.character_relationships = [
            CharacterRelationship.from_dict(
                relationship
            )
            for relationship in data.get(
                "character_relationships",
                [],
            )
        ]

        project.locations = [
            Location.from_dict(location)
            for location in data.get("locations", [])
        ]

        project.episodes = [
            Episode.from_dict(episode)
            for episode in data.get("episodes", [])
        ]

        project.notes = [
            Note.from_dict(note)
            for note in data.get("notes", [])
        ]

        return project

    @classmethod
    def list(cls):
        """Return all project names."""

        cls.PROJECT_DIRECTORY.mkdir(exist_ok=True)

        return sorted(
            file.stem
            for file in cls.PROJECT_DIRECTORY.glob("*.json")
        )

    def rename(self, new_title: str):
        """Rename the project."""

        old_filename = self.filename

        self.title = new_title

        self.save()

        if old_filename.exists():
            old_filename.unlink()

    def delete(self):
        """Delete the project."""

        if self.filename.exists():
            self.filename.unlink()

    #
    # Character methods
    #

    def add_character(self, character: Character):
        self.characters.append(character)

    def find_character(self, name: str):
        for character in self.characters:
            if character.name.lower() == name.lower():
                return character

        return None

    def remove_character(self, name: str):
        character = self.find_character(name)

        if character is not None:
            self.characters.remove(character)

    #
    # Character relationship methods
    #

    def add_character_relationship(
        self,
        relationship: CharacterRelationship,
    ):
        self.character_relationships.append(
            relationship
        )

    #
    # Location methods
    #

    def add_location(self, location: Location):
        self.locations.append(location)

    def find_location(self, name: str):
        for location in self.locations:
            if location.name.lower() == name.lower():
                return location

        return None

    def remove_location(self, name: str):
        location = self.find_location(name)

        if location is not None:
            self.locations.remove(location)

    #
    # Episode methods
    #

    def add_episode(self, episode: Episode):
        self.episodes.append(episode)

    def find_episode(self, title: str):
        for episode in self.episodes:
            if episode.title.lower() == title.lower():
                return episode

        return None

    def remove_episode(self, title: str):
        episode = self.find_episode(title)

        if episode is not None:
            self.episodes.remove(episode)

    #
    # Note methods
    #

    def add_note(self, note: Note):
        self.notes.append(note)

    def find_note(
        self,
        target_type,
        target_id: str,
        title: str,
    ):
        """Find a note for a specific target."""

        for note in self.notes:
            if (
                note.target_type == target_type
                and note.target_id == target_id
                and note.title.lower() == title.lower()
            ):
                return note

        return None

    def find_note_by_title(self, title: str):
        """Find a note by title."""

        for note in self.notes:
            if note.title.lower() == title.lower():
                return note

        return None

    def remove_note(
        self,
        target_type,
        target_id: str,
        title: str,
    ):
        """Remove a note from a specific target."""

        note = self.find_note(
            target_type,
            target_id,
            title,
        )

        if note is not None:
            self.notes.remove(note)