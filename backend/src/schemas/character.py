from pydantic import BaseModel, ConfigDict


class CharacterBase(BaseModel):
    name: str


class CharacterCreate(CharacterBase):
    pass


class CharacterRead(CharacterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
