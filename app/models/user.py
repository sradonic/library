from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, unique=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="users")
    borrowed_books = relationship("BorrowedBook", back_populates="user")
