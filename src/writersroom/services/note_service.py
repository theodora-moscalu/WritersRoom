from writersroom.common.result import Result
from writersroom.domains.story.note import Note
from writersroom.domains.enums.note_target_type import (
    NoteTargetType,
)


class NoteService:
    """Provides business operations for notes."""

    def __init__(self, project):
        self.project = project

    def _create_note(
        self,
        title: str,
        target_type: NoteTargetType,
        target_id: str,
        content: str,
    ) -> Result:
        """Create a note."""

        if (
            self.project.find_note(
                target_type,
                target_id,
                title,
            )
            is not None
        ):
            return Result.fail(
                f"A note called '{title}' already exists for this target."
            )

        note = Note(
            title=title,
            target_type=target_type,
            target_id=target_id,
            content=content,
        )

        self.project.add_note(note)

        self.project.save()

        return Result.ok(
            f"Created note '{title}'.",
            data=note,
        )

    def add_project_note(
        self,
        title: str,
        content: str,
    ) -> Result:
        """Create a project note."""

        return self._create_note(
            title=title,
            target_type=NoteTargetType.PROJECT,
            target_id=self.project.title,
            content=content,
        )

    def add_character_note(
        self,
        character_name: str,
        title: str,
        content: str,
    ) -> Result:
        """Create a character note."""

        character = self.project.find_character(
            character_name
        )

        if character is None:
            return Result.fail(
                f"Character '{character_name}' was not found."
            )

        return self._create_note(
            title=title,
            target_type=NoteTargetType.CHARACTER,
            target_id=character.name,
            content=content,
        )

    def add_location_note(
        self,
        location_name: str,
        title: str,
        content: str,
    ) -> Result:
        """Create a location note."""

        location = self.project.find_location(
            location_name
        )

        if location is None:
            return Result.fail(
                f"Location '{location_name}' was not found."
            )

        return self._create_note(
            title=title,
            target_type=NoteTargetType.LOCATION,
            target_id=location.name,
            content=content,
        )

    def add_episode_note(
        self,
        episode_title: str,
        title: str,
        content: str,
    ) -> Result:
        """Create an episode note."""

        episode = self.project.find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        return self._create_note(
            title=title,
            target_type=NoteTargetType.EPISODE,
            target_id=episode.title,
            content=content,
        )

    def add_scene_note(
        self,
        episode_title: str,
        scene_number: int,
        title: str,
        content: str,
    ) -> Result:
        """Create a scene note."""

        episode = self.project.find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = next(
            (
                scene
                for scene in episode.scenes
                if scene.number == scene_number
            ),
            None,
        )

        if scene is None:
            return Result.fail(
                f"Scene {scene_number} was not found."
            )

        return self._create_note(
            title=title,
            target_type=NoteTargetType.SCENE,
            target_id=f"{episode.title}:{scene.number}",
            content=content,
        )

    def add_relationship_note(
        self,
        relationship,
        title: str,
        content: str,
    ) -> Result:
        """Create a relationship note."""

        if (
            relationship
            not in self.project.character_relationships
        ):
            return Result.fail(
                "Relationship was not found."
            )

        target_id = (
            f"{relationship.source}|"
            f"{relationship.relationship.value}|"
            f"{relationship.target}"
        )

        return self._create_note(
            title=title,
            target_type=NoteTargetType.RELATIONSHIP,
            target_id=target_id,
            content=content,
        )

    def list_notes(self) -> Result:
        """Return all notes."""

        return Result.ok(data=self.project.notes)

    def list_notes_for_target(
        self,
        target_type: NoteTargetType,
        target_id: str,
    ) -> Result:
        """Return notes for a target."""

        notes = [
            note
            for note in self.project.notes
            if note.target_type == target_type
            and note.target_id == target_id
        ]

        return Result.ok(data=notes)

    def show_note(
        self,
        title: str,
    ) -> Result:
        """Return a note."""

        note = self.project.find_note_by_title(
            title
        )

        if note is None:
            return Result.fail(
                f"Note '{title}' was not found."
            )

        return Result.ok(data=note)