from typing import List

from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session

from api.config import get_db
from api.crud.character import character_crud
from api.crud.finish_type import finish_type_crud
from api.schemas.character import CharacterRead
from api.schemas.finish_type import FinishTypeRead

router = APIRouter(prefix="/helpers", tags=["helpers"])


@router.get("/get_characters/", response_model=List[CharacterRead])
def get_characters(db: Session = Depends(get_db)):
    ret = character_crud.get_all(db=db)
    if not ret:
        raise HTTPException(status_code=404, detail="No characters found")
    return ret


@router.get("/get_finish_types/", response_model=List[FinishTypeRead])
def get_finish_types(db: Session = Depends(get_db)):
    ret = finish_type_crud.get_all(db=db)
    if not ret:
        raise HTTPException(status_code=404, detail="No finish types found")
    return ret
