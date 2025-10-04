from pydantic import BaseModel


class User(BaseModel):
    username: str
    disabled: bool | None = None


class UserCreate(User):
    hashed_password: str


class UserUpdate:
    pass
