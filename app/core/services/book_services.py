from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.database import get_db
from app.models import BorrowedBook, Book, User
from app.schemas import Book as BookSchema


def view_all_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> dict:
    book_query = db.query(Book)
    total_count = book_query.count()
    books = book_query.offset(skip).limit(limit).all()
    return {
        "total": total_count,
        "books": [BookSchema.from_orm(book) for book in books]
    }


def view_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    return db.query(Book).filter(Book.id == book_id).first()


def view_books_for_user(user_id: int, db: Session = Depends(get_db)) -> List[BorrowedBook]:
    return db.query(BorrowedBook).filter(BorrowedBook.user_id == user_id).all()


def add_book_to_user(user_id: int, book_id: int, returned_date: Optional[datetime] = None,
                     db: Session = Depends(get_db)) -> BorrowedBook:
    book = db.query(Book).filter(Book.id == book_id).first()
    if book and book.quantity > 0:
        book.quantity -= 1
        today = datetime.utcnow()
        if not returned_date:
            returned_date = today + timedelta(days=14)  # Default to 14 days later if no date provided

        borrowed_book = BorrowedBook(
            user_id=user_id,
            book_id=book_id,
            borrowed_date=today,
            returned_date=returned_date
        )
        db.add(borrowed_book)
        db.commit()
        db.refresh(borrowed_book)
        return borrowed_book
    else:
        raise HTTPException(status_code=400, detail="Book not available")


def delete_book_from_user(borrowed_book_id: int, db: Session = Depends(get_db)) -> None:
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.id == borrowed_book_id).first()
    if borrowed_book:
        book = db.query(Book).filter(Book.id == borrowed_book.book_id).first()
        if book:
            book.quantity += 1
            db.delete(borrowed_book)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        raise HTTPException(status_code=404, detail="Borrowed book not found")


def edit_book_return_date(borrowed_book_id: int, return_date: str, db: Session = Depends(get_db)) -> BorrowedBook:
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.id == borrowed_book_id).first()
    if borrowed_book:
        borrowed_book.returned_date = return_date
        db.commit()
        return borrowed_book
    else:
        raise HTTPException(status_code=404, detail="Borrowed book not found")
