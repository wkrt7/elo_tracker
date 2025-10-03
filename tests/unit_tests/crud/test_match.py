import pytest
from sqlalchemy.orm import Session

from api.crud.match import match_crud
from api.models import MatchParticipant
from api.schemas.match import MatchCreate, MatchParticipantCreate


def test_create_match(db_session: Session, match_data):
    db_match = match_crud.create(db_session, match_data)
    assert db_match.id is not None
    assert db_match.description == match_data.description


def test_get_match(db_session: Session, match_data):
    db_match = match_crud.create(db_session, match_data)
    fetched = match_crud.get(db_session, db_match.id)
    assert fetched.id == db_match.id
    assert fetched.description == db_match.description


def test_list_matches(db_session: Session, match_data):
    match_crud.create(db_session, match_data)
    matches = match_crud.list(db_session)
    assert len(matches) > 0


def test_delete_match(db_session: Session, match_data):
    db_match = match_crud.create(db_session, match_data)
    deleted = match_crud.delete(db_session, db_match.id)
    assert deleted.id == db_match.id
    assert match_crud.get(db_session, db_match.id) is None
