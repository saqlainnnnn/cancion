from cancion.db.session import SessionLocal, engine


def test_engine_exists():
    assert engine is not None


def test_session_factory_exists():
    assert SessionLocal is not None


def test_session_creation():
    session = SessionLocal()

    assert session is not None

    session.close()
