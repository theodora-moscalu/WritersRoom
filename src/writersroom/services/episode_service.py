from writersroom.common.result import Result
from writersroom.domains.story.episode import Episode
from writersroom.domains.story.scene import Scene
from writersroom.services.base_entity_service import BaseEntityService


class EpisodeService(BaseEntityService):
    """Provides business operations for managing episodes."""

    @property
    def entity_name(self) -> str:
        return "Episode"

    def create_entity(self, name: str):
        return Episode(name)

    def find(self, name: str):
        return self.project.find_episode(name)

    def add_to_project(self, episode):
        self.project.add_episode(episode)

    def get_collection(self):
        return self.project.episodes

    def _find_episode(self, title: str):
        """Return an episode or None."""

        return self.project.find_episode(title)

    def _find_scene(
        self,
        episode,
        scene_number: int,
    ):
        """Return a scene from an episode or None."""

        return next(
            (
                scene
                for scene in episode.scenes
                if scene.number == scene_number
            ),
            None,
        )

    def set_logline(self, title: str, logline: str) -> Result:
        episode = self._find_episode(title)

        if episode is None:
            return Result.fail(
                f"Episode '{title}' was not found."
            )

        episode.logline = logline.strip()

        self.project.save()

        return Result.ok(
            f"Updated logline for '{title}'.",
            data=episode,
        )

    def set_synopsis(self, title: str, synopsis: str) -> Result:
        episode = self._find_episode(title)

        if episode is None:
            return Result.fail(
                f"Episode '{title}' was not found."
            )

        episode.synopsis = synopsis.strip()

        self.project.save()

        return Result.ok(
            f"Updated synopsis for '{title}'.",
            data=episode,
        )

    def add_character(
        self,
        episode_title: str,
        character_name: str,
    ) -> Result:
        episode = self._find_episode(episode_title)

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        character = self.project.find_character(character_name)

        if character is None:
            return Result.fail(
                f"Character '{character_name}' was not found."
            )

        if character.name in episode.characters:
            return Result.fail(
                f"'{character.name}' is already in '{episode.title}'."
            )

        episode.characters.append(character.name)

        self.project.save()

        return Result.ok(
            f"Added '{character.name}' to '{episode.title}'.",
            data=episode,
        )

    def add_scene(
        self,
        episode_title: str,
    ) -> Result:
        episode = self._find_episode(episode_title)

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = Scene(
            number=len(episode.scenes) + 1
        )

        episode.scenes.append(scene)

        self.project.save()

        return Result.ok(
            f"Added Scene {scene.number} to '{episode.title}'.",
            data=scene,
        )

    def set_scene_heading(
        self,
        episode_title: str,
        scene_number: int,
        heading: str,
    ) -> Result:

        episode = self._find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = self._find_scene(
            episode,
            scene_number,
        )

        if scene is None:
            return Result.fail(
                f"Scene {scene_number} was not found."
            )

        scene.heading = heading.strip()

        self.project.save()

        return Result.ok(
            f"Updated Scene {scene.number}.",
            data=scene,
        )

    def set_scene_summary(
        self,
        episode_title: str,
        scene_number: int,
        summary: str,
    ) -> Result:

        episode = self._find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = self._find_scene(
            episode,
            scene_number,
        )

        if scene is None:
            return Result.fail(
                f"Scene {scene_number} was not found."
            )

        scene.summary = summary.strip()

        self.project.save()

        return Result.ok(
            f"Updated Scene {scene.number}.",
            data=scene,
        )

    def add_scene_character(
        self,
        episode_title: str,
        scene_number: int,
        character_name: str,
    ) -> Result:

        episode = self._find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = self._find_scene(
            episode,
            scene_number,
        )

        if scene is None:
            return Result.fail(
                f"Scene {scene_number} was not found."
            )

        character = self.project.find_character(
            character_name
        )

        if character is None:
            return Result.fail(
                f"Character '{character_name}' was not found."
            )

        if character.name in scene.characters:
            return Result.fail(
                f"'{character.name}' is already in Scene {scene.number}."
            )

        scene.characters.append(character.name)

        if character.name not in episode.characters:
            episode.characters.append(character.name)

        self.project.save()

        return Result.ok(
            f"Added '{character.name}' to Scene {scene.number}.",
            data=scene,
        )

    def add_scene_location(
        self,
        episode_title: str,
        scene_number: int,
        location_name: str,
    ) -> Result:
        """Attach a location to a scene."""

        episode = self._find_episode(
            episode_title
        )

        if episode is None:
            return Result.fail(
                f"Episode '{episode_title}' was not found."
            )

        scene = self._find_scene(
            episode,
            scene_number,
        )

        if scene is None:
            return Result.fail(
                f"Scene {scene_number} was not found."
            )

        location = self.project.find_location(
            location_name
        )

        if location is None:
            return Result.fail(
                f"Location '{location_name}' was not found."
            )

        if location.name in scene.locations:
            return Result.fail(
                f"'{location.name}' is already in Scene {scene.number}."
            )

        scene.locations.append(location.name)

        if location.name not in episode.locations:
            episode.locations.append(location.name)

        self.project.save()

        return Result.ok(
            f"Added '{location.name}' to Scene {scene.number}.",
            data=scene,
        )

    def show(self, title: str) -> Result:
        episode = self._find_episode(title)

        if episode is None:
            return Result.fail(
                f"Episode '{title}' was not found."
            )

        return Result.ok(data=episode)