from writersroom.draft.draft import Draft, DraftScene


def main():
    print("Testing Draft...")

    draft = Draft(
        scenes=[
            DraftScene(1, "INT. BAR - NIGHT", "Zoe drinks alone.", ["Zoe"]),
            DraftScene(
                2,
                "EXT. STREET - NIGHT",
                "Zoe meets Marcus.",
                ["Zoe", "Marcus"],
            ),
            DraftScene(3, "INT. OFFICE - DAY", "Marcus alone.", ["Marcus"]),
        ]
    )

    assert draft.scene(2).heading == "EXT. STREET - NIGHT"
    assert draft.scene(99) is None
    assert draft.last_scene().number == 3

    assert [s.number for s in draft.preceding(3)] == [1, 2]

    with_zoe = draft.scenes_with_character("zoe")
    assert [s.number for s in with_zoe] == [1, 2]

    assert [s.number for s in draft.scenes_with_character("Marcus")] == [2, 3]

    outline = draft.outline()
    assert outline == [
        "1. INT. BAR - NIGHT — Zoe drinks alone.",
        "2. EXT. STREET - NIGHT — Zoe meets Marcus.",
        "3. INT. OFFICE - DAY — Marcus alone.",
    ]

    print()
    print("Draft tests passed.")


if __name__ == "__main__":
    main()
