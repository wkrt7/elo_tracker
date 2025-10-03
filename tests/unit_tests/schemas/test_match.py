import datetime

import pytest

from api.schemas.match import (
    MatchCreate,
    MatchParticipantCreate,
    MatchParticipantRead,
    MatchParticipantUpdate,
    MatchRead,
    MatchUpdate,
)


def test_match_create():
    match = MatchCreate(team_size=1, k_factor=32, winner_team_side=1)
    assert match.team_size == 1
    assert match.k_factor == 32
    assert match.winner_team_side == 1


def test_match_create_with_optional_fields():
    match = MatchCreate(
        description="Epic showdown", finish_type_id=1, is_long=True, team_size=2, k_factor=40, winner_team_side=2
    )
    assert match.description == "Epic showdown"
    assert match.is_long is True


def test_match_create_draw():
    # winner_team_side can be None for draws
    match = MatchCreate(team_size=1, k_factor=32, winner_team_side=None)
    assert match.winner_team_side is None


def test_match_participant_create():
    mp = MatchParticipantCreate(player_id=2, team_side=1, elo_before=1000, elo_after=1016)
    assert mp.elo_after == 1016
    assert mp.team_side == 1
    assert mp.player_id == 2


def test_match_participant_with_character():
    mp = MatchParticipantCreate(player_id=3, team_side=2, character_id=5, elo_before=1200, elo_after=1185)
    assert mp.character_id == 5


def test_match_read_serialization():
    data = {
        "id": 1,
        "description": None,
        "finish_type_id": None,
        "is_long": False,
        "team_size": 1,
        "k_factor": 32,
        "winner_team_side": 1,
        "date": datetime.datetime.now(),
        "participants": [],
        "match_id": 1,
    }
    match = MatchRead(**data)
    assert match.team_size == 1
    assert match.winner_team_side == 1


def test_match_participant_read_serialization():
    data = {
        "id": 1,
        "match_id": 10,
        "player_id": 5,
        "team_side": 1,
        "character_id": None,
        "elo_before": 1000.0,
        "elo_after": 1016.0,
    }
    mp = MatchParticipantRead(**data)
    assert mp.match_id == 10
    assert mp.elo_after == 1016.0


def test_match_update():
    update = MatchUpdate(description="Updated description", winner_team_side=2)
    assert update.description == "Updated description"
    assert update.winner_team_side == 2


def test_match_update_partial():
    # All fields should be optional
    update = MatchUpdate(description="Only description")
    assert update.description == "Only description"
    assert update.winner_team_side is None


def test_match_participant_update():
    update = MatchParticipantUpdate(character_id=3, team_side=2)
    assert update.character_id == 3
    assert update.team_side == 2


def test_invalid_team_size():
    with pytest.raises(ValueError, match="Team size must be 1-5"):
        MatchCreate(team_size=6, k_factor=32, winner_team_side=1)


def test_invalid_team_size_zero():
    with pytest.raises(ValueError, match="Team size must be 1-5"):
        MatchCreate(team_size=0, k_factor=32, winner_team_side=1)


def test_invalid_team_side():
    with pytest.raises(ValueError, match="Team side must be 1 or 2"):
        MatchParticipantCreate(player_id=1, team_side=3, elo_before=1000, elo_after=1016)


def test_invalid_team_side_zero():
    with pytest.raises(ValueError, match="Team side must be 1 or 2"):
        MatchParticipantCreate(player_id=1, team_side=0, elo_before=1000, elo_after=1016)


def test_invalid_winner_team_side():
    with pytest.raises(ValueError, match="Winner team side must be 1 or 2"):
        MatchCreate(team_size=2, k_factor=32, winner_team_side=5)
