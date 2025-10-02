import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

from backend.src.schemas.character import CharacterCreate
from backend.src.schemas.player import PlayerCreate
from backend.src.schemas.team import TeamCreate, TeamParticipantCreate

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="function")
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(create_test_db):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def new_player_data():
    return PlayerCreate(name=f"TestPlayer_{uuid.uuid4().hex[:8]}")


@pytest.fixture
def new_character_data():
    return CharacterCreate(name=f"Mario_{uuid.uuid4().hex[:8]}")


@pytest.fixture
def new_team_data():
    return TeamCreate(name="Alpha Team")


@pytest.fixture
def new_participant_data(player_id: int, team_id: int):
    return TeamParticipantCreate(player_id=player_id, team_id=team_id)
