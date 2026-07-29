from dataclasses import dataclass

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money


@dataclass(frozen=True, slots=True)
class UpdateContract:
    vendor: str | None = None
    action: Action | None = None
    max_amount: Money | None = None
    frequency: Frequency | None = None
    approval_mode: ApprovalMode | None = None
