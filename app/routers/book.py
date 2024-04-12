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
    view_customer_books
)
from app.core.auth import get_current_active_user
from app.schemas import BorrowedBook, User, Book
from app.constants.user_role import UserRole

router = APIRouter()

@router.get("/books", response_model=dict)
async def get_books_for_user(db: Session = Depends(get_db), skip: int = 0, limit: Optional[int] = None,
                             current_user: User = Depends(get_current_active_user)):
    if current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = view_all_books(db, skip=skip, limit=limit)
    return {"total_books": result["total"], "books": result["books"]}

@router.get("/books/user/{user_id}", response_model=List[BorrowedBook])
async def get_books_for_user(user_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_active_user)):
    if current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return view_books_for_user(user_id, db)

@router.get("/books/mybooks", response_model=List[BorrowedBook])
async def get_my_books(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role.name == "customer":
        return view_books_for_user(current_user.id, db)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.post("/books/user/{user_id}/book/{book_id}")
async def add_book_for_user(user_id: int, book_id: int, returned_date: Optional[datetime] = None,
                            db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return add_book_to_user(user_id, book_id, returned_date, db)

@router.delete("/books/borrowed/{borrowed_book_id}")
async def remove_book_from_user(borrowed_book_id: int, db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_active_user)):
    if current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    delete_book_from_user(borrowed_book_id, db)
    return {"message": "Book successfully removed"}

@router.patch("/books/borrowed/{borrowed_book_id}/return-date/{return_date}")
async def update_book_return_date(borrowed_book_id: int, return_date: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_active_user)):
    if current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return edit_book_return_date(borrowed_book_id, return_date, db)

@router.get("/books/mybooks", response_model=List[BorrowedBook])
async def get_my_books(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return view_customer_books(current_user, db)
