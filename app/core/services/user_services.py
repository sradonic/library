from typing import Optional, Type
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.database.database import get_db
from app.models import User, Role
from app.schemas.user import UserCreate
from app.core.auth.password_security import get_password_hash


def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_role = db.query(Role).filter(Role.name == user.role).first()
    if not db_role:
        raise HTTPException(status_code=400, detail="Role not found")

    db_user = User(
        email=user.email,
        username=user.username,
        name=user.name,
        password=get_password_hash(user.password),
        role_id=db_role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(role: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[
    Type[User]]:
    query = db.query(User)
    if role:
        query = query.join(User.role).filter_by(name=role)
    return query.offset(skip).limit(limit).all()


def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.id == user_id).first()
