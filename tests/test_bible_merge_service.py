from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.episode import Episode
from writersroom.domains.story.project import Project
from writersroom.domains.story.season import Season
from writersroom.extraction.bible_extraction import BibleExtraction
from writersroom.review.review_decision import ReviewDecision
from writersroom.services.bible_pipeline_service import (
    BiblePipelineService,
)


def main():
    print("Testing BiblePipelineService merge...")

    project = Project("The Wine Game")

    project.add_character(
        Character(
            name="Nadia",
            description="The lead.",
            flaw="pride",  # already set — a blank must not overwrite it
        )
    )

    incoming = Character(
        name="Nadia",
        want="respect from the old guard",
        need="to forgive her father",
        flaw="",
    )
    marcus = Character(name="Marcus", description="The mentor.")

    season = Season(number=1, question="Can Nadia be trusted?")

    pilot = Episode(title="Pilot", logline="Nadia arrives.")
    pilot.season = 1
    tasting = Episode(title="The Tasting")
    tasting.season = 1

    extraction = BibleExtraction(
        characters=[incoming, marcus],
        seasons=[season],
        episodes=[pilot, tasting],
        relationships=[
            CharacterRelationship(
                source="Nadia",
                relationship=RelationshipType.MENTORS,
                target="Marcus",
            )
        ],
    )

    service = BiblePipelineService(extractor=object())
    review = service.build_review(extraction, project)

    # reject "The Tasting"
    for item in review.items:
        if item.kind == "episode" and item.proposed.title == "The Tasting":
            item.decision = ReviewDecision.REJECT

    result = service.apply(project, review)
    assert result.success

    merged = project.find_character("Nadia")
    assert merged.want == "respect from the old guard"
    assert merged.need == "to forgive her father"
    assert merged.flaw == "pride"          # preserved
    assert merged.description == "The lead."  # preserved

    assert project.find_character("Marcus") is not None
    assert project.find_season(1).question == "Can Nadia be trusted?"

    titles = [episode.title for episode in project.episodes]
    assert "Pilot" in titles
    assert "The Tasting" not in titles

    assert project.find_season(1).episode_titles == ["Pilot"]
    assert len(project.character_relationships) == 1

    #
    # Re-applying the same review is idempotent (name-keyed, additive)
    #

    service.apply(project, review)
    assert len(project.characters) == 2
    assert len(project.episodes) == 1  # only Pilot was accepted
    assert len(project.character_relationships) == 1
    assert project.find_season(1).episode_titles == ["Pilot"]

    print()
    print(result.message)
    print("BiblePipelineService merge tests passed.")


if __name__ == "__main__":
    main()
