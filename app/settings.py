import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_SHOULD_MIGRATED: bool = (
        os.getenv("DATABASE_SHOULD_MIGRATED", "False") == "True"
    )
    DATABASE_SHOULD_SEEDED: bool = (
        os.getenv("DATABASE_SHOULD_SEEDED", "False") == "True"
    )
