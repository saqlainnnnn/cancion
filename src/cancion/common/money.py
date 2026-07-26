from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable monetary value."""

    amount: Decimal
    currency: str = "USD"

    def __str__(self) -> str:
        return f"{self.currency} {self.amount}"
