from pydantic import BaseModel
from datetime import datetime
from app.schemas import User, Book

class BorrowedBookBase(BaseModel):
    borrowed_date: datetime
    returned_date: datetime
    user_id: int
    book_id: int

class BorrowedBookCreate(BorrowedBookBase):
    pass


class BorrowedBook(BorrowedBookBase):
    id: int
    user: User
    book: Book

    class Config:
        orm_mode = True

