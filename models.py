from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# String isbn;
#   String title;
#   List<String> author;
#   String description;
#   String publisher;
#   List<String> notes;
#   List<String> chapters;

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "books"

    isbn = Column(Integer, primary_key=True, index=True, autoincrement = False)
    notes = Column(String)
    chapters = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="books")