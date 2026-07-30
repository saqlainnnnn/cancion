from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from cancion.db.mappers.agent import (
    to_domain,
    to_model,
)
from cancion.db.models.agent import AgentModel
from cancion.domain.agent import Agent


class AgentRepository:
    """Repository for Agent entities."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        agent: Agent,
    ) -> Agent:
        model = to_model(agent)

        model = self._session.merge(model)

        self._session.commit()

        return to_domain(model)

    def get(
        self,
        agent_id: UUID,
    ) -> Agent | None:
        model = self._session.get(
            AgentModel,
            agent_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def list(self) -> list[Agent]:
        models = self._session.scalars(select(AgentModel)).all()

        return [to_domain(model) for model in models]

    def delete(
        self,
        agent_id: UUID,
    ) -> bool:
        model = self._session.get(
            AgentModel,
            agent_id,
        )

        if model is None:
            return False

        self._session.delete(model)

        self._session.commit()

        return True
