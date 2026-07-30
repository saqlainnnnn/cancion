from uuid import uuid4

from cancion.domain.agent import Agent, AgentStatus


def test_create_agent():
    organization_id = uuid4()

    agent = Agent(
        organization_id=organization_id,
        name="Finance Agent",
        description="Handles invoices",
    )

    assert agent.organization_id == organization_id
    assert agent.name == "Finance Agent"
    assert agent.description == "Handles invoices"
    assert agent.status == AgentStatus.ACTIVE


def test_agent_generates_id():
    organization_id = uuid4()

    agent = Agent(
        organization_id=organization_id,
        name="Finance Agent",
    )

    assert agent.id is not None


def test_agent_generates_timestamps():
    organization_id = uuid4()

    agent = Agent(
        organization_id=organization_id,
        name="Finance Agent",
    )

    assert agent.created_at is not None
    assert agent.updated_at is not None
