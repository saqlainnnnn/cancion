from datetime import UTC

from cancion.api.schemas.agent import AgentResponse
from cancion.db.models.agent import AgentModel
from cancion.domain.agent import Agent


def to_model(agent: Agent) -> AgentModel:
    return AgentModel(
        id=agent.id,
        organization_id=agent.organization_id,
        name=agent.name,
        description=agent.description,
        status=agent.status,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
    )


def to_domain(model: AgentModel) -> Agent:
    return Agent(
        id=model.id,
        organization_id=model.organization_id,
        name=model.name,
        description=model.description,
        status=model.status,
        created_at=_normalize_datetime(model.created_at),
        updated_at=_normalize_datetime(model.updated_at),
    )


def _normalize_datetime(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


def to_agent_response(agent: Agent) -> AgentResponse:
    return AgentResponse(
        id=agent.id,
        organization_id=agent.organization_id,
        name=agent.name,
        description=agent.description,
        status=agent.status,
    )
