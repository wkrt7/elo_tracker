from typing import List, Optional

from sqlalchemy.orm import Session
from src.models import FinishType
from src.schemas.finish_type import FinishTypeCreate, FinishTypeUpdate

from backend.src.crud.base import CRUDBase

finish_type_crud = CRUDBase[FinishType, FinishTypeCreate, FinishTypeUpdate](FinishType)
