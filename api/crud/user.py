from typing import Optional

from crud.base import CRUDBase
from models import User
from schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_username(self, db: Session, username: str, with_transaction: bool = False) -> Optional[User]:
        ret = db.query(User).filter(User.username == username).first()
        if with_transaction and not ret:
            raise ValueError(f"User with username '{username}' does not exist")
        return ret


user_crud = UserCRUD()
