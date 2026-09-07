from pathlib import Path


class DraftCommands:
    """Handles `draft` commands — the link to the writer's script file."""

    def __init__(self, draft_service, project):
        self.draft_service = draft_service
        self.project = project

    def handle(self, args: list[str]):
        """Handle draft commands."""

        if not args:
            self.status()
            return

        action = args[0].lower()

        if action == "link" and len(args) >= 2:
            self.link(" ".join(args[1:]).strip('"'))
            return

        if action == "unlink":
            self.unlink()
            return

        if action == "status":
            self.status()
            return

        if action == "scenes":
            self.scenes()
            return

        if action == "scene" and len(args) >= 2:
            self.scene(args[1])
            return

        self.print_help()

    def link(self, path: str):
        if not Path(path).exists():
            print(f"\nFile not found: {path}\n")
            return

        self.project.draft_path = path
        draft = self.draft_service.current(path)

        if draft is None:
            print(
                "\nLinked, but the file could not be parsed as a script "
                "(export to Fountain).\n"
            )
            return

        print(
            f"\nLinked '{Path(path).name}' — {len(draft.scenes)} scenes.\n"
        )

    def unlink(self):
        self.project.draft_path = ""
        print("\nScript unlinked.\n")

    def status(self):
        print()

        if not self.project.draft_path:
            print("No script linked. Use: draft link <path to .fountain>")
            print()
            return

        draft = self.draft_service.current(self.project.draft_path)

        print(f"Linked: {self.project.draft_path}")

        if draft is None:
            print("Status: file missing or unreadable")
        else:
            print(f"Format: {draft.format}")
            print(f"Scenes: {len(draft.scenes)}")
            print(f"Read:   {draft.read_at}")

        print()

    def scenes(self):
        draft = self._draft()

        if draft is None:
            return

        print()
        print("Scenes")
        print("------")
        for line in draft.outline():
            print(f"  {line}")
        print()

    def scene(self, number: str):
        draft = self._draft()

        if draft is None:
            return

        try:
            scene = draft.scene(int(number))
        except ValueError:
            scene = None

        print()
        if scene is None:
            print(f"No scene {number}.")
        else:
            print(f"SCENE {scene.number}: {scene.heading}")
            print()
            print(scene.text)
        print()

    def _draft(self):
        if not self.project.draft_path:
            print("\nNo script linked.\n")
            return None

        draft = self.draft_service.current(self.project.draft_path)

        if draft is None:
            print("\nThe linked script file is missing or unreadable.\n")

        return draft

    def print_help(self):
        print()
        print("Script commands")
        print("---------------")
        print("draft link <path>    Link a Fountain script file")
        print("draft status         Show the linked script")
        print("draft scenes         List every scene")
        print("draft scene <n>      Show one scene in full")
        print("draft unlink         Forget the linked script")
        print()
