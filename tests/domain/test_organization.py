from datetime import UTC

from cancion.domain.organization import Organization, OrganizationStatus


def test_create_organization():
    organization = Organization(
        name="Acme",
        slug="acme",
    )

    assert organization.name == "Acme"
    assert organization.slug == "acme"
    assert organization.status is OrganizationStatus.ACTIVE


def test_id_is_generated():
    organization = Organization(
        name="Acme",
        slug="acme",
    )

    assert organization.id is not None


def test_timestamps_are_generated():
    organization = Organization(
        name="Acme",
        slug="acme",
    )

    assert organization.created_at.tzinfo == UTC
    assert organization.updated_at.tzinfo == UTC
