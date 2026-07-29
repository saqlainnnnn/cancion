from fastapi import APIRouter, Depends, HTTPException

from cancion.api.dependencies import (
    get_contract_service,
    get_governance_service,
)
from cancion.api.mappers import (
    to_evaluation_response,
    to_spend_request,
)
from cancion.api.schemas.evaluation import (
    EvaluationResponse,
    SpendRequestSchema,
)
from cancion.services.contract import ContractService
from cancion.services.governance import GovernanceService

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
)
def evaluate(
    request: SpendRequestSchema,
    contract_service: ContractService = Depends(
        get_contract_service,
    ),
    governance_service: GovernanceService = Depends(
        get_governance_service,
    ),
) -> EvaluationResponse:
    contract = contract_service.get(request.contract_id)

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail="Contract not found",
        )

    spend_request = to_spend_request(request)

    decision = governance_service.evaluate(
        contract,
        spend_request,
    )

    return to_evaluation_response(decision)
