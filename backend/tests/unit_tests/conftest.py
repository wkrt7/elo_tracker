import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

from backend.src.schemas.character import CharacterCreate
from backend.src.schemas.match import MatchCreate, MatchParticipantCreate
from backend.src.schemas.player import PlayerCreate

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
def db_session(create_test_db: None):
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
def match_data():
    return MatchCreate(
        winner_team_side=1,
        team_size=2,
        k_factor=32.0,
        description="Test Match",
        finish_type_id=None,
        is_long=False,
    )


@pytest.fixture
def participant_data(match_id: int):
    return MatchParticipantCreate(
        player_id=1,  # make sure this player exists
        team_side=1,
        character_id=None,
        elo_before=1000.0,
        elo_after=1016.0,
    )
