from typing import Optional, Type
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.constants.user_role import UserRole
from app.database.database import get_db
from app.models import User, Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.auth.password_security import get_password_hash


def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    check_user_existence(user.username, user.email, db)
    db_role = db.query(Role).filter(Role.name == UserRole.customer).first()
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


def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user_data).items():
        if value is not None:
            if var == 'role':
                role_instance = db.query(Role).filter_by(name=value).first()
                if role_instance:
                    setattr(db_user, var, role_instance)
                else:
                    raise HTTPException(status_code=404, detail="Role not found")
            else:
                setattr(db_user, var, value)

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


def check_user_existence(username: str, email: str, db: Session):
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    if existing_user:
        if existing_user.email == email:
            raise HTTPException(status_code=400, detail="A user with this email already exists.")
        elif existing_user.username == username:
            raise HTTPException(status_code=400, detail="A user with this username already exists.")