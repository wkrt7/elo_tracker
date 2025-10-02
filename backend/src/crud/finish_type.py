from typing import List, Optional

from sqlalchemy.orm import Session
from src.models import FinishType
from src.schemas.finish_type import FinishTypeCreate


def get_finish_type(db: Session, finish_type_id: int) -> Optional[FinishType]:
    return db.query(FinishType).filter(FinishType.id == finish_type_id).first()


def get_finish_types(db: Session, skip: int = 0, limit: int = 100) -> List[FinishType]:
    return db.query(FinishType).offset(skip).limit(limit).all()


def create_finish_type(db: Session, finish_type: FinishTypeCreate) -> FinishType:
    db_finish_type = FinishType(name=finish_type.name)
    db.add(db_finish_type)
    db.commit()
    db.refresh(db_finish_type)
    return db_finish_type


def delete_finish_type(db: Session, finish_type_id: int) -> Optional[FinishType]:
    db_finish_type = get_finish_type(db, finish_type_id)
    if not db_finish_type:
        return None
    db.delete(db_finish_type)
    db.commit()
    return db_finish_type


def update_finish_type(db: Session, finish_type_id: int, data) -> FinishType:
    raise NotImplementedError("Update operation is not implemented yet")
