from writersroom.commands.base_entity_commands import BaseEntityCommands


class LocationCommands(BaseEntityCommands):
    """Handles all location-related commands."""

    def __init__(self, service):
        super().__init__("location", service)

    @property
    def entity_name(self) -> str:
        return "Location"

    @property
    def entity_name_plural(self) -> str:
        return "Locations"