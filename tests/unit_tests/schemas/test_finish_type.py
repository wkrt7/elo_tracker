import pytest

from api.schemas.finish_type import FinishTypeCreate, FinishTypeRead


def test_finish_type_create():
    f = FinishTypeCreate(name="Knockout")
    assert f.name == "Knockout"


def test_finish_type_read():
    data = {"id": 1, "name": "Knockout"}
    f = FinishTypeRead(**data)
    assert f.id == 1
