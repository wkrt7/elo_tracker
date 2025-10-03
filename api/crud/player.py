from typing import List, Optional

from psycopg2 import IntegrityError
from sqlalchemy.orm import Session

from api.crud.base import CRUDBase
from api.models import Player
from api.schemas.player import PlayerCreate, PlayerUpdate


class PlayerCRUD(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    def __init__(self):
        super().__init__(Player)

    def batch_get_by_names(self, db: Session, names: List[str], with_transaction: bool = False) -> List[Player]:
        ret = db.query(Player).filter(Player.name.in_(names)).all()
        if with_transaction:
            if len(ret) != len(names):
                missing_names = set(names) - {player.name for player in ret}
                raise ValueError(f"Players with names {missing_names} do not exist")
        return ret

    def get_player_by_name(self, db: Session, name: str) -> Optional[Player]:
        return db.query(Player).filter(Player.name == name).first()

    def create(self, db: Session, obj_in: PlayerCreate) -> Player:
        if self.get_player_by_name(db, obj_in.name):
            raise ValueError(f"Player with name '{obj_in.name}' already exists")
        return super().create(db, obj_in)


player_crud = PlayerCRUD()
