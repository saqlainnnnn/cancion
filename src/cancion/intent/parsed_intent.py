from dataclasses import dataclass

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money


@dataclass(slots=True)
class ParsedIntent:
    """Mutable intermediate parsing result."""

    vendor: str | None = None
    action: Action | None = None
    amount: Money | None = None
    frequency: Frequency | None = None
    approval_mode: ApprovalMode = ApprovalMode.AUTO
