from pydantic import BaseModel, ConfigDict, field_validator


class CharacterBase(BaseModel):
    name: str

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Character name cannot be empty")
        return v


class CharacterCreate(CharacterBase):
    pass


class CharacterRead(CharacterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
