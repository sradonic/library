from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.constants.user_role import UserRole


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserRole), default=UserRole.customer)
    users = relationship("User", back_populates="role")
