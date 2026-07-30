from datetime import UTC, datetime
from uuid import uuid4

from cancion.domain.organization import (
    Organization,
    OrganizationStatus,
)
from cancion.repositories.organization import OrganizationRepository


def make_organization() -> Organization:
    now = datetime.now(UTC)

    return Organization(
        id=uuid4(),
        name="Acme Inc.",
        slug="acme-inc",
        status=OrganizationStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )


def test_save_and_get(session) -> None:
    repo = OrganizationRepository(session)

    organization = make_organization()

    repo.save(organization)

    loaded = repo.get(organization.id)

    assert loaded == organization


def test_list(session) -> None:
    repo = OrganizationRepository(session)

    organization = make_organization()

    repo.save(organization)

    organizations = repo.list()

    assert len(organizations) == 1
    assert organizations[0] == organization


def test_delete(session) -> None:
    repo = OrganizationRepository(session)

    organization = make_organization()

    repo.save(organization)

    assert repo.delete(organization.id)

    assert repo.get(organization.id) is None
