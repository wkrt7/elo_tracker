import pytest
from sqlalchemy.orm import Session

from api.crud.match import match_crud
from api.models import MatchParticipant
from api.schemas.match import MatchCreate, MatchInternal, MatchParticipantCreate


def test_create_match(db_session: Session, match_data):
    m = MatchInternal(**match_data.model_dump(), k_factor=32)
    db_match = match_crud.create(db_session, m)
    assert db_match.id is not None
    assert db_match.description == match_data.description


def test_get_match(db_session: Session, match_data):
    m = MatchInternal(**match_data.model_dump(), k_factor=32)
    db_match = match_crud.create(db_session, m)
    fetched = match_crud.get(db_session, db_match.id)
    assert fetched.id == db_match.id
    assert fetched.description == db_match.description


def test_list_matches(db_session: Session, match_data):
    m = MatchInternal(**match_data.model_dump(), k_factor=32)
    db_match = match_crud.create(db_session, m)
    matches = match_crud.list(db_session)
    assert len(matches) > 0


def test_delete_match(db_session: Session, match_data):
    m = MatchInternal(**match_data.model_dump(), k_factor=32)
    db_match = match_crud.create(db_session, m)
    deleted = match_crud.delete(db_session, db_match.id)
    assert deleted.id == db_match.id
    assert match_crud.get(db_session, db_match.id) is None
