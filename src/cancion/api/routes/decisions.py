from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from cancion.api.dependencies import get_decision_service
from cancion.api.mappers.decision import to_decision_response
from cancion.api.schemas.decision import DecisionResponse
from cancion.services.decision import DecisionService

router = APIRouter()


@router.get(
    "/",
    response_model=list[DecisionResponse],
)
def list_decisions(
    service: DecisionService = Depends(get_decision_service),
) -> list[DecisionResponse]:
    """List all decisions."""

    decisions = service.list()

    return [to_decision_response(decision) for decision in decisions]


@router.get(
    "/{decision_id}",
    response_model=DecisionResponse,
)
def get_decision(
    decision_id: UUID,
    service: DecisionService = Depends(get_decision_service),
) -> DecisionResponse:
    """Get a decision by its ID."""

    decision = service.get(decision_id)

    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found",
        )

    return to_decision_response(decision)


@router.get(
    "/contracts/{contract_id}",
    response_model=list[DecisionResponse],
)
def list_contract_decisions(
    contract_id: UUID,
    service: DecisionService = Depends(get_decision_service),
) -> list[DecisionResponse]:
    """List all decisions for a contract."""

    decisions = service.list_by_contract(contract_id)

    return [to_decision_response(decision) for decision in decisions]


@router.delete(
    "/{decision_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_decision(
    decision_id: UUID,
    service: DecisionService = Depends(get_decision_service),
) -> Response:
    """Delete a decision."""

    deleted = service.delete(decision_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
