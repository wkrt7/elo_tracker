from typing import Generic, List, Optional, Protocol, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDProtocol(Protocol[ModelType, CreateSchemaType, UpdateSchemaType]):
    def get(self, db: "Session", id: int) -> Optional[ModelType]: ...
    def list(self, db: "Session", skip: int = 0, limit: int = 100) -> List[ModelType]: ...
    def create(self, db: "Session", obj_in: CreateSchemaType) -> ModelType: ...
    def update(self, db: "Session", id: int, obj_in) -> ModelType: ...
    def delete(self, db: "Session", id: int) -> Optional[ModelType]: ...


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: type[ModelType]

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int, with_transaction: bool = False) -> Optional[ModelType]:
        ret = db.query(self.model).filter(self.model.id == id).first()
        if with_transaction and ret is None:
            raise ValueError(f"Object with id {id} does not exist")
        return ret

    def batch_get(self, db: Session, ids: List[int], with_transaction: bool = False) -> List[ModelType]:
        ret = db.query(self.model).filter(self.model.id.in_(ids)).all()

        if with_transaction:
            if len(ret) != len(ids):
                missing_ids = set(ids) - {obj.id for obj in ret}
                raise ValueError(f"Objects with ids {missing_ids} do not exist")
        return ret

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = self.get(db, id)
        if not db_obj:
            raise ValueError(f"Object with id {id} does not exist")
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
        db.flush()
        return db_obj
