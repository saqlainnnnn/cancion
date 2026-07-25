from typing import Protocol

from cancion.domain.intent import Intent


class IntentParser(Protocol):
    """Protocol implemented by all intent parsers."""

    def parse(self, message: str) -> Intent: ...
