from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    author = Column(String(255), index=True)
    quantity = Column(Integer)

    borrowed_books = relationship("BorrowedBook", back_populates="book")