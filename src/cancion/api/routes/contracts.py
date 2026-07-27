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


@router.get("/")
def list_contracts() -> list:
    return []


@router.get("/{contract_id}")
def get_contract(contract_id: str) -> dict[str, str]:
    return {"contract_id": contract_id}


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
