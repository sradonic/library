from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.database import Base

class BorrowedBook(Base):
    __tablename__ = "borrowedbooks"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    borrowed_date = Column(Date)
    returned_date = Column(Date)
    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")
