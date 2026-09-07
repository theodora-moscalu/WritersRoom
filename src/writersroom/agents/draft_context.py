import re


class DraftContextBuilder:
    """Feeds the Showrunner the scene being worked on, plus the outline."""

    def __init__(self, draft_service, scene_char_cap: int = 4000):
        self.draft_service = draft_service
        self.scene_char_cap = scene_char_cap

    def build(self, project, focus_text: str) -> str:
        """Return a CURRENT DRAFT block, or '' when nothing is linked."""

        draft = self.draft_service.current(project.draft_path)

        if draft is None or not draft.scenes:
            return ""

        focus, reason = self._focus_scene(draft, project, focus_text)

        scene_text = focus.text

        if len(scene_text) > self.scene_char_cap:
            scene_text = scene_text[: self.scene_char_cap] + "\n[...]"

        header = (
            f"CURRENT DRAFT — {len(draft.scenes)} scenes, "
            f"focus scene {focus.number} ({reason})"
        )

        return "\n".join(
            [
                header,
                "",
                f"SCENE {focus.number}: {focus.heading}",
                scene_text,
                "",
                "OUTLINE",
                *(f"  {line}" for line in draft.outline()),
            ]
        )

    def _focus_scene(self, draft, project, focus_text: str):
        """Resolve the scene in focus and why: number, character, edit, or last."""

        match = re.search(
            r"\bscene\s+(\d+)\b|\b(\d+)[.:]",
            focus_text,
            re.IGNORECASE,
        )

        if match:
            number = int(match.group(1) or match.group(2))
            scene = draft.scene(number)
            if scene is not None:
                return scene, "named"

        lowered = focus_text.lower()

        for character in project.characters:
            if re.search(
                r"\b" + re.escape(character.name.lower()) + r"\b",
                lowered,
            ):
                scenes = draft.scenes_with_character(character.name)
                if scenes:
                    return scenes[-1], f"most recent with {character.name}"

        changed = draft.latest_change()
        if changed is not None:
            return changed, "just edited"

        return draft.last_scene(), "last scene"
