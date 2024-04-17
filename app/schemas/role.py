from pydantic import BaseModel

from app.constants.user_role import UserRole


class RoleBase(BaseModel):
    name: UserRole


class Role(RoleBase):
    id: int
