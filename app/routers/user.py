from typing import Annotated, List, Optional
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter, HTTPException, status
from app.core.auth import get_current_active_user, RoleChecker
from app.schemas import User, UserCreate
from app.constants.user_role import UserRole
from app.core.services import create_user, get_users, get_user_by_id
from app.database.database import get_db

router = APIRouter()


@router.get("/users/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/users/", response_model=User, dependencies=[Depends(RoleChecker([UserRole.admin]))])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user=user, db=db)


@router.get("/users/", response_model=List[User],
            dependencies=[Depends(RoleChecker([UserRole.admin, UserRole.librarian]))])
async def list_users(role: Optional[UserRole] = None, skip: int = 0, limit: Optional[int] = None,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    if current_user.role.name == UserRole.librarian.value:
        if role and role != UserRole.customer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        elif not role:
            role = UserRole.customer

    return get_users(role=role.value if role else None, skip=skip, limit=limit, db=db)


@router.get("/users/{user_id}", response_model=User)
async def read_user_details(user_id: int, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)):
    db_user = get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the current user is allowed to view the requested user's details
    if current_user.role.name == UserRole.librarian and db_user.role.name != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    elif current_user.role.name not in [UserRole.admin, UserRole.librarian]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    return db_user
