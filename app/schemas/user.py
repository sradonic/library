from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.schemas.role import Role
from app.constants.user_role import UserRole


class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.customer

    @field_validator('password')
    def password_complexity_check(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class User(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

    @field_validator('role')
    def validate_role(cls, v):
        if v:
            return UserRole[v.lower()]
        return None

    class Config:
        from_attributes = True
