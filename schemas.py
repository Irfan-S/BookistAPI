from typing import List, Optional

from pydantic import BaseModel

# TODO create chapter base and test.

class BookBase(BaseModel):
    notes :Optional[str] =""
    chapters :Optional[str] =""


class BookCreate(BookBase):
    isbn: int


class Book(BookCreate):
    owner_id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    books: List[Book] = []

    class Config:
        orm_mode = True