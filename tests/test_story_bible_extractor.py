from writersroom.agents.story_bible_extractor import (
    StoryBibleExtractor,
)


BIBLE = """
===== SLIDE 1 =====
TITLE: THE WINE GAME

===== SLIDE 2 =====
TITLE: NADIA — Lead
BODY:
- A sommelier, 34, sharp and self-taught
- Wants: to be accepted by the old-money wine establishment
- Needs: to stop measuring her worth by their approval
- Flaw: she is contemptuous of anyone who inherited their status
- Arc: outsider, to insider, to exposed fraud, to something honest
NOTES: Grew up above her father's failing wine shop.

===== SLIDE 3 =====
TITLE: MARCUS — Mentor / Antagonist
BODY:
- A revered critic who takes Nadia under his wing
- Secretly the source of the forged provenance she starts selling

===== SLIDE 4 =====
TITLE: SEASON 1
BODY:
- Central question: will the old guard ever truly accept Nadia?
- Theme: belonging has a price
- Arc: Nadia climbs, then the forgery she built her name on begins to unravel

===== SLIDE 5 =====
TITLE: EPISODES
BODY:
- 1x01 "The Blind Tasting" — Nadia humiliates a rival and catches Marcus's eye
- 1x02 "Provenance" — Nadia sells her first bottle with a story she cannot verify
"""


def main():
    print("Testing StoryBibleExtractor...")

    extraction = StoryBibleExtractor().extract(BIBLE)

    for warning in extraction.warnings:
        print("  !", warning)

    names = {c.name.lower() for c in extraction.characters}
    assert "nadia" in names
    assert "marcus" in names

    nadia = next(
        c for c in extraction.characters if c.name.lower() == "nadia"
    )
    assert nadia.want
    assert nadia.flaw

    assert len(extraction.seasons) == 1
    assert extraction.seasons[0].question

    episode_titles = {e.title.lower() for e in extraction.episodes}
    assert any("tasting" in title for title in episode_titles)

    print()
    print(
        f"characters={len(extraction.characters)} "
        f"relationships={len(extraction.relationships)} "
        f"seasons={len(extraction.seasons)} "
        f"episodes={len(extraction.episodes)}"
    )
    print(f"Nadia.want: {nadia.want}")
    print(f"Season 1 question: {extraction.seasons[0].question}")
    print()
    print("StoryBibleExtractor tests passed.")


if __name__ == "__main__":
    main()
