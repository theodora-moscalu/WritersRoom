from writersroom.common.result import Result
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.services.base_entity_service import (
    BaseEntityService,
)


class CharacterRelationshipService(BaseEntityService):
    """Business logic for character relationships."""

    @property
    def entity_name(self) -> str:
        return "Relationship"

    def create_entity(self, name: str):
        raise NotImplementedError(
            "Relationships cannot be created with a single name."
        )

    def find(self, name: str):
        return None

    def add_to_project(self, relationship):
        self.project.add_character_relationship(
            relationship
        )

    def get_collection(self):
        return self.project.character_relationships

    def add_relationship(
        self,
        source: str,
        relationship,
        target: str,
    ) -> Result:
        """Create a relationship between two characters."""

        source_character = self.project.find_character(
            source
        )

        if source_character is None:
            return Result.fail(
                f"Character '{source}' was not found."
            )

        target_character = self.project.find_character(
            target
        )

        if target_character is None:
            return Result.fail(
                f"Character '{target}' was not found."
            )

        if source.lower() == target.lower():
            return Result.fail(
                "A character cannot have a relationship with themselves."
            )

        for existing in self.project.character_relationships:

            if (
                existing.source.lower()
                == source.lower()
                and existing.target.lower()
                == target.lower()
                and existing.relationship
                == relationship
            ):
                return Result.fail(
                    "That relationship already exists."
                )

        relationship_object = CharacterRelationship(
            source=source_character.name,
            relationship=relationship,
            target=target_character.name,
        )

        self.project.add_character_relationship(
            relationship_object
        )

        self.project.save()

        return Result.ok(
            "Relationship added.",
            data=relationship_object,
        )