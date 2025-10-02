from src.models import Character
from src.schemas.character import CharacterCreate

from backend.src.crud.base import CRUDBase

character_crud = CRUDBase[Character, CharacterCreate](Character)
