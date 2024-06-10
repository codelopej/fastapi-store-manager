from sqlmodel import create_engine
from app.settings import Settings

should_echo = False if Settings.ENV == "production" else True
engine = create_engine(Settings.DATABASE_URL, echo=should_echo)
