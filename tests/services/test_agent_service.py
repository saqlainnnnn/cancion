from uuid import uuid4

from cancion.domain.agent import (
    Agent,
    AgentStatus,
)
from cancion.repositories.agent import AgentRepository
from cancion.services.agent import AgentService


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


def make_service(session):
    repository = AgentRepository(session)
    return AgentService(repository)


def test_create_agent(session):
    service = make_service(session)

    agent = make_agent()

    created = service.create(agent)

    assert created == agent
    assert service.get(created.id) == agent


def test_get_agent(session):
    service = make_service(session)

    agent = make_agent()

    service.create(agent)

    loaded = service.get(agent.id)

    assert loaded == agent


def test_list_agents(session):
    service = make_service(session)

    service.create(make_agent(name="Finance"))
    service.create(make_agent(name="HR"))

    agents = service.list()

    assert len(agents) == 2


def test_update_agent(session):
    service = make_service(session)

    agent = make_agent()

    service.create(agent)

    updated = Agent(
        id=agent.id,
        organization_id=agent.organization_id,
        name="Finance Agent v2",
        description="Updated description",
        status=agent.status,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
    )

    service.update(updated)

    loaded = service.get(agent.id)

    assert loaded == updated


def test_delete_agent(session):
    service = make_service(session)

    agent = make_agent()

    service.create(agent)

    assert service.delete(agent.id)
    assert service.get(agent.id) is None
