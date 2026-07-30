from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from cancion.api.dependencies import get_agent_service
from cancion.api.schemas.agent import (
    AgentResponse,
    CreateAgentRequest,
    UpdateAgentRequest,
)
from cancion.db.mappers.agent import to_agent_response
from cancion.domain.agent import Agent
from cancion.services.agent import AgentService

router = APIRouter()


@router.get("/", response_model=list[AgentResponse])
def list_agents(
    service: AgentService = Depends(get_agent_service),
):
    return [to_agent_response(agent) for agent in service.list()]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: UUID,
    service: AgentService = Depends(get_agent_service),
):
    agent = service.get(agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return to_agent_response(agent)


@router.post(
    "/",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    request: CreateAgentRequest,
    service: AgentService = Depends(get_agent_service),
):
    agent = Agent(
        organization_id=request.organization_id,
        name=request.name,
        description=request.description,
    )

    return to_agent_response(service.create(agent))


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
)
def update_agent(
    agent_id: UUID,
    request: UpdateAgentRequest,
    service: AgentService = Depends(get_agent_service),
):
    agent = service.get(agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    updated = Agent(
        id=agent.id,
        organization_id=agent.organization_id,
        name=request.name,
        description=request.description,
        status=agent.status,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
    )

    return to_agent_response(service.update(updated))


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_agent(
    agent_id: UUID,
    service: AgentService = Depends(get_agent_service),
):
    deleted = service.delete(agent_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
