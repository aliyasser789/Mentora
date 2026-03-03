import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> int:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL is not set in .env or environment.", file=sys.stderr)
        return 1

    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ DB connection OK")
        return 0
    except Exception as exc:
        print(f"❌ DB connection failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
