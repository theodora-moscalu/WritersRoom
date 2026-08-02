from abc import ABC, abstractmethod


class BaseCommandHandler(ABC):
    """Base class for all command handlers."""

    def __init__(self, name: str):
        self.name = name
        self.commands = {}

    def handle(self, command: str):
        """Handle a command."""

        parts = command.split(maxsplit=1)

        if not parts:
            self.print_help()
            return

        action = parts[0].lower()

        handler = self.commands.get(action)

        if handler is None:
            self.unknown_command(action)
            return

        argument = ""

        if len(parts) > 1:
            argument = parts[1]

        handler(argument)

    def unknown_command(self, action: str):
        """Display an unknown command message."""

        print(f"\nUnknown {self.name} command: {action}\n")

    @abstractmethod
    def print_help(self):
        """Display help for this command handler."""
        pass