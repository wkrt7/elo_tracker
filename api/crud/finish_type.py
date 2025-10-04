from crud.base import CRUDBase
from models import FinishType
from schemas.finish_type import FinishTypeCreate, FinishTypeUpdate
from sqlalchemy.orm import Session

finish_type_crud = CRUDBase[FinishType, FinishTypeCreate, FinishTypeUpdate](FinishType)
