from writersroom.domains.story.episode import Episode
from writersroom.domains.story.project import Project
from writersroom.domains.story.season import Season


def main():
    print("Testing Season...")

    project = Project("The Wine Game")

    season = Season(
        number=1,
        title="Foundations",
        logline="Zoe builds her reputation on a lie.",
        arc="From outsider to insider to exposed.",
        question="Will the old guard ever accept Zoe?",
        theme="Belonging has a price.",
    )

    project.add_season(season)
    project.add_episode(Episode("Pilot"))
    season.add_episode_title("Pilot")
    season.add_episode_title("Pilot")  # idempotent

    assert len(season.episode_titles) == 1

    reloaded = Project.from_dict(project.to_dict())

    assert len(reloaded.seasons) == 1

    loaded = reloaded.find_season(1)

    assert loaded.title == "Foundations"
    assert loaded.question == "Will the old guard ever accept Zoe?"
    assert loaded.episode_titles == ["Pilot"]

    reloaded.remove_season(1)
    assert reloaded.find_season(1) is None

    print()
    print("Season tests passed.")


if __name__ == "__main__":
    main()
