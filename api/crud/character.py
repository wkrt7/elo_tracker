from api.crud.base import CRUDBase
from api.models import Character
from api.schemas.character import CharacterCreate, CharacterUpdate

character_crud = CRUDBase[Character, CharacterCreate, CharacterUpdate](Character)
