from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.services import (
    view_books_for_user,
    view_all_books,
    add_book_to_user,
    delete_book_from_user,
    edit_book_return_date,
    view_book
)
from app.core.auth import get_current_active_user, RoleChecker
from app.schemas import BorrowedBook, User, Book
from app.constants.user_role import UserRole

router = APIRouter()

dependencies_admin_librarian = [Depends(RoleChecker([UserRole.admin, UserRole.librarian]))]


@router.get("/books/mybooks", response_model=List[BorrowedBook])
async def get_my_books(current_user: User = Depends(get_current_active_user),
                       db: Session = Depends(get_db)):
    if current_user.role.name == "customer":
        return view_books_for_user(current_user.id, db)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@router.get("/books", response_model=dict, dependencies=dependencies_admin_librarian)
async def get_books(db: Session = Depends(get_db),
                    skip: int = 0, limit: Optional[int] = None):
    result = view_all_books(db, skip=skip, limit=limit)
    return {"total_books": result["total"], "books": result["books"]}


@router.get("/books/{book_id}", response_model=Book, dependencies=dependencies_admin_librarian)
async def get_book(book_id: int,
                   db: Session = Depends(get_db)):
    return view_book(book_id, db)


@router.get("/books/user/{user_id}", response_model=List[BorrowedBook], dependencies=dependencies_admin_librarian)
async def get_books_for_user(user_id: int,
                             db: Session = Depends(get_db)):
    return view_books_for_user(user_id, db)


@router.post("/books/user/{user_id}/book/{book_id}", dependencies=dependencies_admin_librarian)
async def add_book_for_user(user_id: int, book_id: int,
                            returned_date: Optional[datetime] = None,
                            db: Session = Depends(get_db)):
    return add_book_to_user(user_id, book_id, returned_date, db)


@router.delete("/books/borrowed/{borrowed_book_id}", dependencies=dependencies_admin_librarian)
async def remove_book_from_user(borrowed_book_id: int,
                                db: Session = Depends(get_db)):
    delete_book_from_user(borrowed_book_id, db)
    return {"message": "Book successfully removed"}


@router.patch("/books/borrowed/{borrowed_book_id}/return-date/{return_date}", dependencies=dependencies_admin_librarian)
async def update_book_return_date(borrowed_book_id: int, return_date: str,
                                  db: Session = Depends(get_db)):
    return edit_book_return_date(borrowed_book_id, return_date, db)



