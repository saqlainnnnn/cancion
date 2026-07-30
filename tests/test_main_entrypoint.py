from cancion.main import app


def test_app_entrypoint_is_available() -> None:
    assert app is not None
