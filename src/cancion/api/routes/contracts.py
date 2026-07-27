from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cancion.api.dependencies import (
    get_contract_service,
    get_intent_parser,
)
from cancion.api.mappers import to_contract_response
from cancion.api.schemas.contract import (
    ContractResponse,
    CreateContractRequest,
)
from cancion.intent.exceptions import IntentParseError
from cancion.intent.protocol import IntentParser
from cancion.services.contract import ContractService

router = APIRouter()


@router.get(
    "/",
    response_model=list[ContractResponse],
)
def list_contracts(
    service: ContractService = Depends(get_contract_service),
) -> list[ContractResponse]:
    """List all contracts."""

    contracts = service.list()

    return [to_contract_response(contract) for contract in contracts]


@router.get(
    "/{contract_id}",
    response_model=ContractResponse,
)
def get_contract(
    contract_id: UUID,
    service: ContractService = Depends(get_contract_service),
) -> ContractResponse:
    """Get a contract by its ID."""

    contract = service.get(contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    return to_contract_response(contract)


@router.post(
    "/",
    response_model=ContractResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contract(
    request: CreateContractRequest,
    parser: IntentParser = Depends(get_intent_parser),
    service: ContractService = Depends(get_contract_service),
) -> ContractResponse:
    try:
        intent = parser.parse(request.text)
    except IntentParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    contract = service.create(intent)

    return to_contract_response(contract)


@router.delete("/{contract_id}")
def delete_contract(contract_id: str) -> dict[str, str]:
    return {"deleted": contract_id}
