import pytest
from src.schemas.player import PlayerRead
from src.schemas.team import TeamCreate, TeamParticipantCreate, TeamRead


def test_team_create():
    team = TeamCreate(name="TeamX")
    assert team.name == "TeamX"


def test_team_read_serialization():
    data = {"id": 1, "name": "TeamX", "participants": []}
    team = TeamRead(**data)
    assert team.id == 1
    assert isinstance(team.participants, list)


def test_team_participant_create():
    tp = TeamParticipantCreate(team_id=1, player_id=2)
    assert tp.team_id == 1
    assert tp.player_id == 2
