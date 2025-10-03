from typing import List, Optional

from sqlalchemy.orm import Session

from api.crud.base import CRUDBase
from api.models import FinishType
from api.schemas.finish_type import FinishTypeCreate, FinishTypeUpdate

finish_type_crud = CRUDBase[FinishType, FinishTypeCreate, FinishTypeUpdate](FinishType)
