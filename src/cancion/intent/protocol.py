from typing import Protocol

from cancion.domain.intent import Intent


class IntentParser(Protocol):
    """Converts natural language into an Intent."""

    def parse(self, message: str) -> Intent:
        """Parse a user message into an Intent."""
        ...
