from decimal import Decimal

from pydantic import BaseModel

from cancion.common import Action, ApprovalMode, Frequency


class UpdateContractRequest(BaseModel):
    vendor: str | None = None
    action: Action | None = None

    max_amount: Decimal | None = None
    frequency: Frequency | None = None

    approval_mode: ApprovalMode | None = None
