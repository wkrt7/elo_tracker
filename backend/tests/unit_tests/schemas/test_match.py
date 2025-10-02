import datetime

import pytest
from src.schemas.match import MatchCreate, MatchParticipantCreate, MatchRead
from src.schemas.team import TeamRead


def test_match_create():
    match = MatchCreate(team_a_id=1, team_b_id=2, team_size=1, k_factor=32)
    assert match.team_a_id == 1
    assert match.team_b_id == 2


def test_match_participant_create():
    mp = MatchParticipantCreate(match_id=1, player_id=2, team_id=1, elo_before=1000, elo_after=1016)
    assert mp.elo_after == 1016


def test_match_read_serialization():
    data = {
        "id": 1,
        "team_a": {"id": 1, "name": "A", "participants": []},
        "team_b": {"id": 2, "name": "B", "participants": []},
        "description": None,
        "is_long": False,
        "team_size": 1,
        "k_factor": 32,
        "winner_team_id": None,
        "date": datetime.datetime.now(),
    }
    match = MatchRead(**data)
    assert match.team_size == 1
