from sqlmodel import SQLModel
from app.settings import Settings
from app.database.db import engine
from .seed import create_warehouses


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__" and Settings.DATABASE_SHOULD_MIGRATED:
    create_db_and_tables()

    if Settings.DATABASE_SHOULD_SEEDED:
        create_warehouses(engine)
