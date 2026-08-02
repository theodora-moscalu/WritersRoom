from writersroom.commands.base_entity_commands import BaseEntityCommands


class CharacterCommands(BaseEntityCommands):
    """Handles all character-related commands."""

    def __init__(self, service):
        super().__init__("character", service)

    @property
    def entity_name(self) -> str:
        return "Character"

    @property
    def entity_name_plural(self) -> str:
        return "Characters"