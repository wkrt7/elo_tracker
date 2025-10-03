import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ID = os.getenv("DB_ID")
DB_URL = os.getenv("DB_URL")
DB_PORT = os.getenv("DB_PORT")

connection_string = f"postgresql://postgres.{DB_ID}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/postgres"

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
