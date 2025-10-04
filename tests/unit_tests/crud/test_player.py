import pytest
from sqlalchemy.orm import Session

from api.crud.player import player_crud
from api.models import Player
from api.schemas.player import PlayerCreate


def test_create_player(db_session: Session, new_player_data):
    db_player = player_crud.create(db_session, new_player_data)
    assert db_player.id is not None
    assert db_player.name == new_player_data.name
    assert db_player.elo == 1200.0


def test_get_player(db_session: Session, new_player_data):
    db_player = player_crud.create(db_session, new_player_data)
    fetched = player_crud.get(db_session, db_player.id)
    assert fetched.id == db_player.id
    assert fetched.name == db_player.name


def test_get_player_by_name(db_session: Session, new_player_data):
    db_player = player_crud.create(db_session, new_player_data)
    fetched = player_crud.get_player_by_name(db_session, db_player.name)
    assert fetched.id == db_player.id


def test_get_players(db_session: Session, new_player_data):
    player_crud.create(db_session, new_player_data)
    player_crud.create(db_session, PlayerCreate(name=f"{new_player_data.name}_2"))
    players = player_crud.get_all(db_session)
    assert len(players) > 1


def test_delete_player(db_session: Session, new_player_data):
    db_player = player_crud.create(db_session, new_player_data)
    deleted = player_crud.delete(db_session, db_player.id)
    assert deleted.id == db_player.id
    assert deleted.name == db_player.name
    assert player_crud.get(db_session, db_player.id) is None
