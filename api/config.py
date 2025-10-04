import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ID = os.getenv("DB_ID")
DB_URL = os.getenv("DB_URL")
DB_PORT = int(os.getenv("DB_PORT", "0"))

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

STARTING_ELO = int(os.getenv("STARTING_ELO", 1200))
K_FACTOR_LONG = float(os.getenv("K_FACTOR", 50.0))
K_FACTOR_SHORT = float(os.getenv("K_FACTOR_SHORT", 40.0))

connection_string = (
    f"postgresql://postgres.{DB_ID}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/postgres"
)

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
