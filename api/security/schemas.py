from pydantic import BaseModel
from typing import Optional


class UserIn(BaseModel):
    user_name: str
    user_pass: str


class UserOut(BaseModel):
    id: int
    user_name: str


class UserUpdate(UserIn):
    new_user_name: str = None
    new_user_pass: str = None
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
