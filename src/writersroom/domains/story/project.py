from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import CharacterRelationship
from writersroom.domains.story.episode import Episode
from writersroom.domains.story.location import Location
from writersroom.domains.story.note import Note
from writersroom.domains.story.season import Season


class Project:
    """Represents a WritersRoom project (one series / one workspace)."""

    def __init__(
        self,
        title: str,
        identity: str | None = None,
        created: str | None = None,
        updated: str | None = None,
    ):
        self.title = title
        self.identity = identity
        self.created = created
        self.updated = updated

        self.draft_path = ""
        self.conversation_history = []
        self.characters = []
        self.character_relationships = []
        self.locations = []
        self.episodes = []
        self.seasons = []
        self.notes = []

    def to_dict(self):
        """Convert the project's story data to a dictionary."""

        return {
            "title": self.title,
            "draft_path": self.draft_path,
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
            "seasons": [
                season.to_dict()
                for season in self.seasons
            ],
            "notes": [
                note.to_dict()
                for note in self.notes
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data,
        identity: str | None = None,
        created: str | None = None,
        updated: str | None = None,
    ):
        """Create a Project from a dictionary."""

        project = cls(
            title=data["title"],
            identity=identity,
            created=created,
            updated=updated,
        )

        project.draft_path = data.get("draft_path", "")

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

        project.seasons = [
            Season.from_dict(season)
            for season in data.get("seasons", [])
        ]

        project.notes = [
            Note.from_dict(note)
            for note in data.get("notes", [])
        ]

        return project

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
    # Season methods
    #

    def add_season(self, season: Season):
        self.seasons.append(season)

    def find_season(self, number: int):
        for season in self.seasons:
            if season.number == number:
                return season

        return None

    def remove_season(self, number: int):
        season = self.find_season(number)

        if season is not None:
            self.seasons.remove(season)

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
