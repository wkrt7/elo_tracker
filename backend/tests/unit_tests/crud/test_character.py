import pytest
from sqlalchemy.orm import Session
from src.crud.character import character_crud
from src.models import Character
from src.schemas.character import CharacterCreate


def test_create_character(db_session: Session, new_character_data):
    db_char = character_crud.create(db_session, new_character_data)
    assert db_char.id is not None
    assert db_char.name == new_character_data.name


def test_get_character(db_session: Session, new_character_data):
    db_char = character_crud.create(db_session, new_character_data)
    fetched = character_crud.get(db_session, db_char.id)
    assert fetched.id == db_char.id


def test_delete_character(db_session: Session, new_character_data):
    db_char = character_crud.create(db_session, new_character_data)
    deleted = character_crud.delete(db_session, db_char.id)
    assert deleted.id == db_char.id
    assert character_crud.get(db_session, db_char.id) is None


def test_character_name_empty(db_session: Session):
    with pytest.raises(ValueError) as excinfo:
        new_character_data = CharacterCreate(name="   ")
        character_crud.create(db_session, new_character_data)
    assert "Character name cannot be empty" in str(excinfo.value)


def test_get_nonexistent_character(db_session: Session):
    fetched = character_crud.get(db_session, 9999)
    assert fetched is None


def test_character_unique_name(db_session: Session, new_character_data):
    character_crud.create(db_session, new_character_data)
    with pytest.raises(Exception) as excinfo:
        character_crud.create(db_session, new_character_data)
    assert "UNIQUE constraint failed" in str(excinfo.value) or "duplicate key value violates unique constraint" in str(
        excinfo.value
    )


def test_character_name_whitespace(db_session: Session):
    new_character_data = CharacterCreate(name="   Hero   ")
    db_char = character_crud.create(db_session, new_character_data)
    assert db_char.name == "   Hero   "
