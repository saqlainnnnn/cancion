from cancion.core.config import Settings, get_settings


def test_default_settings():
    settings = Settings()

    assert settings.APP_NAME == "Cancion"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.API_V1_PREFIX == "/api/v1"


def test_settings_cached():
    first = get_settings()
    second = get_settings()

    assert first is second


def test_database_url_exists():
    settings = Settings()

    assert settings.DATABASE_URL.startswith("postgresql")
