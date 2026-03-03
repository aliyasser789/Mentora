import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")


class Config:
    """Base configuration loaded from environment variables."""

    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    @classmethod
    def validate(cls, config: dict) -> None:
        missing = [key for key in ("DATABASE_URL", "JWT_SECRET") if not config.get(key)]
        if missing:
            names = ", ".join(missing)
            raise RuntimeError(
                f"Missing required environment variable(s): {names}. "
                "Create backend/.env from backend/.env.example."
            )

