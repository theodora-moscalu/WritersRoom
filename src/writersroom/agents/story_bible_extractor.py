from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.domains.enums.note_target_type import (
    NoteTargetType,
)
from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character import (
    Character,
)
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.relationship_beat import (
    RelationshipBeat,
)
from writersroom.domains.story.episode import (
    Episode,
)
from writersroom.domains.story.location import (
    Location,
)
from writersroom.domains.story.note import (
    Note,
)
from writersroom.domains.story.season import (
    Season,
)
from writersroom.extraction.bible_extraction import (
    BibleExtraction,
)
from writersroom.llm.llm_factory import (
    create_extraction_llm,
)


class StoryBibleExtractor(Agent):
    """Turns a series bible document into structured project data."""

    def __init__(self):
        super().__init__(
            name="Story Bible Archivist",
            prompt_file="story_bible_extractor.txt",
            llm=create_extraction_llm(),
        )

    def extract(self, bible_text: str) -> BibleExtraction:
        """Extract structured entities from bible text."""

        data = self.llm.respond_json(
            [
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": bible_text,
                },
            ]
        )

        warnings: list[str] = []

        return BibleExtraction(
            characters=self._characters(data),
            relationships=self._relationships(data, warnings),
            seasons=self._seasons(data),
            episodes=self._episodes(data, warnings),
            locations=self._locations(data),
            notes=self._notes(data),
            warnings=warnings,
        )

    #
    # Per-category mapping
    #

    def _characters(self, data: dict) -> list[Character]:
        result = []

        for entry in data.get("characters", []):

            name = (entry.get("name") or "").strip()

            if not name:
                continue

            result.append(
                Character(
                    name=name,
                    description=entry.get("description", ""),
                    traits=[
                        trait
                        for trait in entry.get("traits", [])
                        if trait
                    ],
                    want=entry.get("want", ""),
                    need=entry.get("need", ""),
                    flaw=entry.get("flaw", ""),
                    arc=entry.get("arc", ""),
                    backstory=entry.get("backstory", ""),
                    voice=entry.get("voice", ""),
                )
            )

        return result

    def _relationships(
        self,
        data: dict,
        warnings: list[str],
    ) -> list[CharacterRelationship]:
        result = []

        for entry in data.get("relationships", []):

            source = (entry.get("source") or "").strip()
            target = (entry.get("target") or "").strip()
            raw_type = (entry.get("type") or "").strip()

            if not (source and target and raw_type):
                continue

            relationship_type = self._relationship_type(raw_type)

            if relationship_type is None:
                warnings.append(
                    f"Skipped relationship '{source} - {raw_type} - {target}': "
                    "unrecognised type."
                )
                continue

            result.append(
                CharacterRelationship(
                    source=source,
                    relationship=relationship_type,
                    target=target,
                    history=[
                        RelationshipBeat(
                            episode=beat.get("episode", ""),
                            description=beat.get("description", ""),
                            becomes=beat.get("becomes", ""),
                        )
                        for beat in entry.get("history", [])
                        if beat.get("description") or beat.get("becomes")
                    ],
                )
            )

        return result

    def _relationship_type(self, raw: str):
        lowered = raw.lower()

        for candidate in RelationshipType:
            if candidate.value.lower() == lowered:
                return candidate

        for candidate in RelationshipType:
            if (
                candidate.value.lower() in lowered
                or lowered in candidate.value.lower()
            ):
                return candidate

        return None

    def _seasons(self, data: dict) -> list[Season]:
        result = []

        for entry in data.get("seasons", []):

            number = entry.get("number")

            if not isinstance(number, int):
                continue

            result.append(
                Season(
                    number=number,
                    title=entry.get("title", ""),
                    logline=entry.get("logline", ""),
                    arc=entry.get("arc", ""),
                    question=entry.get("question", ""),
                    theme=entry.get("theme", ""),
                )
            )

        return result

    def _episodes(
        self,
        data: dict,
        warnings: list[str],
    ) -> list[Episode]:
        result = []

        for entry in data.get("episodes", []):

            title = (entry.get("title") or "").strip()

            if not title:
                continue

            episode = Episode(
                title=title,
                logline=entry.get("logline", ""),
                synopsis=entry.get("synopsis", ""),
                a_story=entry.get("a_story", ""),
                b_story=entry.get("b_story", ""),
                episode_arc=entry.get("episode_arc", ""),
            )

            episode.season = entry.get("season", 1)

            result.append(episode)

        return result

    def _locations(self, data: dict) -> list[Location]:
        result = []

        for entry in data.get("locations", []):

            name = (entry.get("name") or "").strip()

            if name:
                result.append(Location(name))

        return result

    def _notes(self, data: dict) -> list[Note]:
        result = []

        for entry in data.get("notes", []):

            title = (entry.get("title") or "").strip()
            content = (entry.get("content") or "").strip()

            if not (title and content):
                continue

            target = (entry.get("target") or "project").strip().lower()

            target_type = NoteTargetType.PROJECT
            target_id = "project"

            if target.startswith("character:"):
                target_type = NoteTargetType.CHARACTER
                target_id = entry["target"].split(":", 1)[1].strip()
            elif target.startswith("season:") and not title.lower().startswith(
                "season"
            ):
                title = f"Season {target.split(':', 1)[1].strip()} — {title}"

            result.append(
                Note(
                    title=title,
                    target_type=target_type,
                    target_id=target_id,
                    content=content,
                )
            )

        return result
