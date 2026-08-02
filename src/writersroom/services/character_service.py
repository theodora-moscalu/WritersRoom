from writersroom.domains.story.character import Character
from writersroom.services.base_entity_service import BaseEntityService


class CharacterService(BaseEntityService):
    """Provides business operations for managing characters."""

    @property
    def entity_name(self) -> str:
        return "Character"

    def create_entity(self, name: str):
        return Character(name)

    def find(self, name: str):
        return self.project.find_character(name)

    def add_to_project(self, character):
        self.project.add_character(character)

    def get_collection(self):
         return self.project.characters