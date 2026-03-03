from __future__ import annotations

from flask import Flask
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.db_handeling.config import Config

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None
_scoped_session: scoped_session[Session] | None = None


def _ensure_engine(
    database_url: str | None = None,
    echo: bool | None = None,
) -> Engine:
    global _engine
    if _engine is None:
        resolved_url = database_url or Config.DATABASE_URL
        if not resolved_url:
            raise RuntimeError(
                "DATABASE_URL is not set. Create backend/.env from backend/.env.example."
            )
        resolved_echo = Config.SQLALCHEMY_ECHO if echo is None else echo
        _engine = create_engine(
            resolved_url,
            echo=resolved_echo,
            future=True,
            pool_pre_ping=True,
        )
    return _engine


def get_engine() -> Engine:
    """Return the shared SQLAlchemy engine."""
    return _ensure_engine()


def get_session() -> scoped_session[Session]:
    """Return a shared scoped session factory."""
    global _session_factory, _scoped_session
    if _scoped_session is None:
        _session_factory = sessionmaker(
            bind=_ensure_engine(),
            autoflush=False,
            autocommit=False,
            future=True,
        )
        _scoped_session = scoped_session(_session_factory)
    return _scoped_session


def _remove_session() -> None:
    if _scoped_session is not None:
        _scoped_session.remove()


class SQLAlchemyExtension:
    """Lightweight SQLAlchemy integration for Flask app factory."""

    def __init__(self) -> None:
        self.engine = None
        self.session = None

    def init_app(self, app: Flask) -> None:
        self.engine = _ensure_engine(
            database_url=app.config.get("DATABASE_URL"),
            echo=app.config.get("SQLALCHEMY_ECHO", Config.SQLALCHEMY_ECHO),
        )
        self.session = get_session()

        app.extensions["db"] = self
        app.teardown_appcontext(self._teardown_session)

    def _teardown_session(self, exception: BaseException | None = None) -> None:
        _remove_session()


db = SQLAlchemyExtension()

