import datetime

import pytest
from pydantic import ValidationError

from api.schemas.player import PlayerCreate, PlayerRead


def test_player_create_valid():
    player = PlayerCreate(name="Alice")
    assert player.name == "Alice"


def test_player_create_invalid():
    with pytest.raises(ValidationError):
        PlayerCreate(name=123)  # must be str


def test_player_read_serialization():
    data = {
        "id": 1,
        "name": "Alice",
        "elo": 1000.0,
        "created_at": datetime.datetime.now(datetime.UTC),
    }
    player = PlayerRead(**data)
    assert player.id == 1
    assert player.elo == 1000.0
