from uuid import uuid4

from cancion.domain.agent import (
    Agent,
    AgentStatus,
)
from cancion.repositories.agent import AgentRepository


def make_agent(
    organization_id=None,
    name: str = "Finance Agent",
    description: str = "Handles invoices",
) -> Agent:
    return Agent(
        organization_id=organization_id or uuid4(),
        name=name,
        description=description,
        status=AgentStatus.ACTIVE,
    )


def test_save_agent(session):
    repository = AgentRepository(session)

    agent = make_agent()

    saved = repository.save(agent)

    assert saved == agent


def test_get_agent(session):
    repository = AgentRepository(session)

    agent = make_agent()

    repository.save(agent)

    loaded = repository.get(agent.id)

    assert loaded == agent


def test_list_agents(session):
    repository = AgentRepository(session)

    repository.save(make_agent(name="Finance"))
    repository.save(make_agent(name="HR"))

    agents = repository.list()

    assert len(agents) == 2


def test_delete_agent(session):
    repository = AgentRepository(session)

    agent = make_agent()

    repository.save(agent)

    assert repository.delete(agent.id)
    assert repository.get(agent.id) is None
