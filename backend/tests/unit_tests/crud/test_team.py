import pytest
from sqlalchemy.orm import Session
from src.crud import player as player_crud
from src.crud import team as team_crud
from src.models import TeamParticipant
from src.schemas.team import TeamCreate, TeamParticipantCreate

from backend.src.schemas.player import PlayerCreate


def test_create_team(db_session: Session, new_team_data):
    db_team = team_crud.create_team(db_session, new_team_data)
    assert db_team.id is not None
    assert db_team.name == new_team_data.name


def test_get_team(db_session: Session, new_team_data):
    db_team = team_crud.create_team(db_session, new_team_data)
    fetched = team_crud.get_team(db_session, db_team.id)
    assert fetched.id == db_team.id
    assert fetched.name == new_team_data.name


def test_get_teams(db_session: Session, new_team_data):
    team_crud.create_team(db_session, new_team_data)
    teams = team_crud.get_teams(db_session)
    assert len(teams) > 0


def test_add_team_participant_invalid_player(db_session: Session, new_team_data):
    db_team = team_crud.create_team(db_session, new_team_data)
    invalid_participant_data = TeamParticipantCreate(player_id=9999, team_id=db_team.id)  # Assuming 9999 does not exist

    with pytest.raises(Exception) as excinfo:
        team_crud.add_team_participant(db_session, invalid_participant_data)
    assert "does not exist" in str(excinfo.value) or "insert or update on table" in str(excinfo.value)


def test_add_team_participant(db_session: Session, new_team_data):
    db_team = team_crud.create_team(db_session, new_team_data)
    # Assume there is a player with id=1 in the test DB

    new_palyer = player_crud.create_player(db_session, PlayerCreate(name="ParticipantPlayer"))
    participant_data = TeamParticipantCreate(player_id=new_palyer.id, team_id=db_team.id)
    db_participant = team_crud.add_team_participant(db_session, participant_data)

    assert isinstance(db_participant, TeamParticipant)
    assert db_participant.team_id == db_team.id


def test_update_team_not_implemented(db_session: Session, new_team_data):
    db_team = team_crud.create_team(db_session, new_team_data)

    with pytest.raises(NotImplementedError):
        team_crud.update_team(db_session, db_team.id, data=None)
