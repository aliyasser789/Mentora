from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Alembic Config object (reads alembic.ini)
config = context.config

# Configure Python logging from config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Resolve backend/.env reliably ---
# This file is: backend/app/db_handeling/migrations/env.py
# parents[0]=migrations, [1]=db_handeling, [2]=app, [3]=backend
BACKEND_DIR = Path(__file__).resolve().parents[3]

# Ensure `backend/` is on sys.path so `import app...` works
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Load backend/.env explicitly
load_dotenv(BACKEND_DIR / ".env")

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Configure backend/.env before running Alembic."
    )

# Tell Alembic the DB URL (overrides any hardcoded value in alembic.ini)
config.set_main_option("sqlalchemy.url", database_url)

# --- Import SQLAlchemy metadata ---
from app.db_handeling.db import Base  # noqa: E402
from app.db_handeling.db import models  # noqa: E402,F401  (ensures model files are imported)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()