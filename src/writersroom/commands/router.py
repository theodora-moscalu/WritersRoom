class CommandRouter:
    """Routes top-level commands to the appropriate command handler."""

    def __init__(self):
        self.handlers = {}

    def register(self, command: str, handler):
        """Register a handler for a top-level command."""

        self.handlers[command.lower()] = handler

    def dispatch(self, command: str) -> bool:
        """
        Dispatch a command.

        Returns True if a handler processed the command.
        """

        parts = command.split()

        if not parts:
            return False

        handler = self.handlers.get(parts[0].lower())

        if handler is None:
            return False

        handler.handle(parts[1:])

        return True