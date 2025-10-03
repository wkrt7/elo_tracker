from src.models import Character
from src.schemas.character import CharacterCreate, CharacterUpdate

from backend.src.crud.base import CRUDBase

character_crud = CRUDBase[Character, CharacterCreate, CharacterUpdate](Character)
