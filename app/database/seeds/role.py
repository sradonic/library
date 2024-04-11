from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.role import Role
from app.constants.user_role import UserRole

roles = [UserRole.admin, UserRole.customer, UserRole.librarian]


def add_roles_to_db(db: Session = SessionLocal()):
    for role_name in roles:
        # Check if the role already exists
        existing_role = db.query(Role).filter_by(name=role_name).first()
        if not existing_role:
            db_role = Role(name=role_name)
            db.add(db_role)
    db.commit()


if __name__ == "__main__":
    add_roles_to_db()
