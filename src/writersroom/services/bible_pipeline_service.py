from writersroom.agents.story_bible_extractor import (
    StoryBibleExtractor,
)
from writersroom.common.result import (
    Result,
)
from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.review.bible_review import (
    BibleReview,
    BibleReviewItem,
)


class BiblePipelineService:
    """Imports a series bible document into structured project knowledge."""

    _SCALAR_FIELDS = {
        "character": (
            "description",
            "want",
            "need",
            "flaw",
            "arc",
            "backstory",
            "voice",
        ),
        "season": (
            "title",
            "logline",
            "arc",
            "question",
            "theme",
        ),
        "episode": (
            "logline",
            "synopsis",
            "a_story",
            "b_story",
            "episode_arc",
        ),
        "note": ("content",),
    }

    def __init__(self, extractor: StoryBibleExtractor | None = None):
        self._extractor = extractor

    @property
    def extractor(self) -> StoryBibleExtractor:
        """Build the extractor lazily so startup does not need an API key."""

        if self._extractor is None:
            self._extractor = StoryBibleExtractor()

        return self._extractor

    #
    # Extract
    #

    def extract(self, path: str, project) -> BibleReview:
        """Read a bible document and match its entities against the project."""

        importer = ImporterFactory.create(path)
        imported = importer.import_document(path)

        extraction = self.extractor.extract(imported.text)

        return self.build_review(extraction, project)

    def build_review(self, extraction, project) -> BibleReview:
        """Match extracted entities against the project into a review."""

        review = BibleReview(warnings=extraction.warnings)

        for character in extraction.characters:
            review.items.append(
                BibleReviewItem(
                    kind="character",
                    proposed=character,
                    existing=project.find_character(character.name),
                )
            )

        for season in extraction.seasons:
            review.items.append(
                BibleReviewItem(
                    kind="season",
                    proposed=season,
                    existing=project.find_season(season.number),
                )
            )

        for episode in extraction.episodes:
            review.items.append(
                BibleReviewItem(
                    kind="episode",
                    proposed=episode,
                    existing=project.find_episode(episode.title),
                )
            )

        for location in extraction.locations:
            review.items.append(
                BibleReviewItem(
                    kind="location",
                    proposed=location,
                    existing=project.find_location(location.name),
                )
            )

        for relationship in extraction.relationships:
            review.items.append(
                BibleReviewItem(
                    kind="relationship",
                    proposed=relationship,
                    existing=self._find_relationship(project, relationship),
                )
            )

        for note in extraction.notes:
            review.items.append(
                BibleReviewItem(
                    kind="note",
                    proposed=note,
                    existing=project.find_note_by_title(note.title),
                )
            )

        return review

    #
    # Apply
    #

    def apply(self, project, review: BibleReview) -> Result:
        """Merge the accepted entities into the project by name (additive)."""

        counts = {
            "added": 0,
            "updated": 0,
        }

        for item in review.accepted_items:

            handler = getattr(self, f"_apply_{item.kind}")
            handler(project, item, counts)

        self._link_episodes_to_seasons(project, review)

        return Result.ok(
            f"Applied bible: {counts['added']} added, "
            f"{counts['updated']} updated.",
            data=counts,
        )

    def _apply_character(self, project, item, counts):
        existing = project.find_character(item.proposed.name)

        if existing is None:
            project.add_character(item.proposed)
            counts["added"] += 1
            return

        self._merge_scalars(existing, item.proposed, "character")
        self._merge_list(existing, item.proposed, "traits")
        counts["updated"] += 1

    def _apply_season(self, project, item, counts):
        existing = project.find_season(item.proposed.number)

        if existing is None:
            project.add_season(item.proposed)
            counts["added"] += 1
            return

        self._merge_scalars(existing, item.proposed, "season")
        counts["updated"] += 1

    def _apply_episode(self, project, item, counts):
        existing = project.find_episode(item.proposed.title)

        if existing is None:
            project.add_episode(item.proposed)
            counts["added"] += 1
            return

        self._merge_scalars(existing, item.proposed, "episode")
        counts["updated"] += 1

    def _apply_location(self, project, item, counts):
        if project.find_location(item.proposed.name) is None:
            project.add_location(item.proposed)
            counts["added"] += 1

    def _apply_relationship(self, project, item, counts):
        if self._find_relationship(project, item.proposed) is None:
            project.add_character_relationship(item.proposed)
            counts["added"] += 1

    def _apply_note(self, project, item, counts):
        existing = project.find_note_by_title(item.proposed.title)

        if existing is None:
            project.add_note(item.proposed)
            counts["added"] += 1
            return

        if item.proposed.content:
            existing.content = item.proposed.content
        counts["updated"] += 1

    #
    # Merge helpers
    #

    def _merge_scalars(self, existing, proposed, kind: str):
        """Overwrite a field only when the bible gives a non-empty value."""

        for name in self._SCALAR_FIELDS[kind]:

            value = getattr(proposed, name, "")

            if value:
                setattr(existing, name, value)

    def _merge_list(self, existing, proposed, name: str):
        target = getattr(existing, name)

        for value in getattr(proposed, name, []):
            if value not in target:
                target.append(value)

    def _find_relationship(self, project, relationship):
        for existing in project.character_relationships:
            if (
                existing.source.lower() == relationship.source.lower()
                and existing.target.lower() == relationship.target.lower()
                and existing.relationship == relationship.relationship
            ):
                return existing

        return None

    def _link_episodes_to_seasons(self, project, review: BibleReview):
        for item in review.accepted_items:

            if item.kind != "episode":
                continue

            number = getattr(item.proposed, "season", 1)
            season = project.find_season(number)

            if season is not None:
                season.add_episode_title(item.proposed.title)
