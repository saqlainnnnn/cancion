from cancion.core.logging import logger


def test_logger_exists():
    assert logger is not None


def test_logger_has_info():
    assert hasattr(logger, "info")


def test_logger_has_error():
    assert hasattr(logger, "error")
