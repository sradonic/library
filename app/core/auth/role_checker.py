from fastapi import Depends, HTTPException, status
from .authentication import get_current_user, get_current_active_user
from app.models import User


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = [role.value for role in allowed_roles]

    async def __call__(self, user: User = Depends(get_current_user)):
        user_role_name = user.role.name if user.role else None
        if user_role_name not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")


async def get_current_user_role(current_user: User = Depends(get_current_active_user)) -> str:
    return current_user.role.name



