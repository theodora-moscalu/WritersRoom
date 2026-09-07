from dataclasses import dataclass
from dataclasses import field

from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.episode import Episode
from writersroom.domains.story.location import Location
from writersroom.domains.story.note import Note
from writersroom.domains.story.season import Season


@dataclass
class BibleExtraction:
    """Structured entities proposed from a series bible."""

    characters: list[Character] = field(default_factory=list)
    relationships: list[CharacterRelationship] = field(default_factory=list)
    seasons: list[Season] = field(default_factory=list)
    episodes: list[Episode] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(
            [
                self.characters,
                self.relationships,
                self.seasons,
                self.episodes,
                self.locations,
                self.notes,
            ]
        )
