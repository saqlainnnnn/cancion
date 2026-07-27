from cancion.api.schemas.common import MoneyResponse
from cancion.api.schemas.contract import ContractResponse
from cancion.domain.contract import Contract


def to_contract_response(contract: Contract) -> ContractResponse:
    """Convert a domain Contract into an API response."""

    return ContractResponse(
        id=contract.id,
        vendor=contract.vendor,
        action=contract.action,
        max_amount=MoneyResponse(
            amount=contract.max_amount.amount,
            currency=contract.max_amount.currency,
        ),
        frequency=contract.frequency,
        approval_mode=contract.approval_mode,
        status=contract.status,
        version=contract.version,
        agent_id=contract.agent_id,
        created_at=contract.created_at,
        updated_at=contract.updated_at,
    )
