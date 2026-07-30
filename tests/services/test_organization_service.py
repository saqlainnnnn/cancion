from cancion.domain.organization import (
    Organization,
    OrganizationStatus,
)
from cancion.repositories.organization import OrganizationRepository
from cancion.services.organization import OrganizationService


def make_organization(
    name: str = "Acme",
    slug: str = "acme",
) -> Organization:
    return Organization(
        name=name,
        slug=slug,
        status=OrganizationStatus.ACTIVE,
    )


def make_service(session):
    repository = OrganizationRepository(session)
    return OrganizationService(repository)


def test_create_organization(session):
    service = make_service(session)

    organization = make_organization()

    created = service.create(organization)

    assert created == organization
    assert service.get(created.id) == organization


def test_get_organization(session):
    service = make_service(session)

    organization = make_organization()

    service.create(organization)

    loaded = service.get(organization.id)

    assert loaded == organization


def test_list_organizations(session):
    service = make_service(session)

    service.create(make_organization("Acme", "acme"))
    service.create(make_organization("OpenAI", "openai"))

    organizations = service.list()

    assert len(organizations) == 2


def test_update_organization(session):
    service = make_service(session)

    organization = make_organization()

    service.create(organization)

    updated = Organization(
        id=organization.id,
        name="Acme Corporation",
        slug="acme",
        status=organization.status,
        created_at=organization.created_at,
        updated_at=organization.updated_at,
    )

    service.update(updated)

    loaded = service.get(organization.id)

    assert loaded == updated


def test_delete_organization(session):
    service = make_service(session)

    organization = make_organization()

    service.create(organization)

    assert service.delete(organization.id)
    assert service.get(organization.id) is None
