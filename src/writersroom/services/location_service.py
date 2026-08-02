from writersroom.domains.story.location import Location
from writersroom.services.base_entity_service import BaseEntityService


class LocationService(BaseEntityService):
    """Provides business operations for managing locations."""

    @property
    def entity_name(self) -> str:
        return "Location"

    def create_entity(self, name: str):
        return Location(name)

    def find(self, name: str):
        return self.project.find_location(name)

    def add_to_project(self, location):
        self.project.add_location(location)

    def get_collection(self):
        return self.project.locations