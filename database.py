from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
