from uuid import UUID

from cancion.domain.agent import Agent
from cancion.repositories.agent import AgentRepository


class AgentService:
    """Application service for agents."""

    def __init__(
        self,
        repository: AgentRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        agent: Agent,
    ) -> Agent:
        return self._repository.save(agent)

    def get(
        self,
        agent_id: UUID,
    ) -> Agent | None:
        return self._repository.get(agent_id)

    def list(self) -> list[Agent]:
        return self._repository.list()

    def update(
        self,
        agent: Agent,
    ) -> Agent:
        return self._repository.save(agent)

    def delete(
        self,
        agent_id: UUID,
    ) -> bool:
        return self._repository.delete(agent_id)
