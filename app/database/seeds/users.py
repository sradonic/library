from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models import Role, User
from app.constants.user_role import UserRole
from passlib.context import CryptContext

admin_email = "admin@example.com"
admin_password = "Secret123!"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_default_admin_user(db: Session = SessionLocal()):
    admin_role = db.query(Role).filter_by(name=UserRole.admin).first()

    existing_user = db.query(User).filter_by(email=admin_email).first()
    if not existing_user and admin_role:
        hashed_password = pwd_context.hash(admin_password)
        new_user = User(
            username="admin",
            name="Admin User",
            email="admin@example.com",
            password=hashed_password,
            role_id=admin_role.id
        )
        db.add(new_user)
        db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    add_default_admin_user(db)
