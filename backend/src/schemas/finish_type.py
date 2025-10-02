from pydantic import BaseModel, ConfigDict


class FinishTypeBase(BaseModel):
    name: str


class FinishTypeCreate(FinishTypeBase):
    pass


class FinishTypeRead(FinishTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FinishTypeUpdate(FinishTypeBase):
    pass
