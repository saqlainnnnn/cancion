from dataclasses import dataclass

from cancion.common import ApprovalMode, Frequency
from cancion.common.money import Money


@dataclass(frozen=True, slots=True)
class Intent:
    """Represents a validated spending intent."""

    vendor: str
    action: str
    max_amount: Money
    frequency: Frequency

    approval_mode: ApprovalMode = ApprovalMode.AUTO
