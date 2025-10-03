from crud.base import CRUDBase
from models import Character
from schemas.character import CharacterCreate, CharacterUpdate

character_crud = CRUDBase[Character, CharacterCreate, CharacterUpdate](Character)
