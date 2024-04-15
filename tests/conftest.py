import pytest
from datetime import timedelta, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.core.config import settings
from app.core.auth import get_password_hash, create_access_token
from app.models import User, Role, Book, BorrowedBook
from app.constants.user_role import UserRole


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(settings.test_database_url)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield TestingSessionLocal

    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(test_db):
    db_session = test_db()
    try:
        yield db_session
    finally:
        db_session.close()

@pytest.fixture
def roles(session):
    roles = {
        'admin': Role(name=UserRole.admin.value),
        'customer': Role(name=UserRole.customer.value),
        'librarian': Role(name=UserRole.librarian.value)
    }
    session.add_all(roles.values())
    session.commit()
    return roles


@pytest.fixture
def admin_user(session, roles):
    hashed_password = get_password_hash("Securepassword1")
    user = User(username="admin_user", name="Admin User", email="admin@example.com", password=hashed_password,
                role_id=roles['admin'].id)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def customer_user(session, roles):
    hashed_password = get_password_hash("Customerpassword1")
    user = User(username="customer_user", name="Customer User", email="customer@example.com", password=hashed_password,
                role_id=roles['customer'].id)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def librarian_user(session, roles):
    hashed_password = get_password_hash("librarianpassword1")
    user = User(username="librarian_user", name="Librarian User", email="librarian@example.com",
                password=hashed_password,
                role_id=roles['librarian'].id)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def generate_token():
    def _generate_token(user):
        return create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))

    return _generate_token


@pytest.fixture
def make_customer(session, customer_user):
    hashed_password = get_password_hash("existingPassword1")
    user = User(
        username="existingUser",
        email="existing@example.com",
        name="Existing User",
        password=hashed_password,
        role_id=customer_user.role_id
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def create_books(session):
    def _create_books(count):
        books = []
        for i in range(count):
            book = Book(title=f"Book {i+1}", author=f"Author {i+1}", quantity=10+i, description=f"Description {i+1}")
            session.add(book)
            books.append(book)
        session.commit()
        return books
    return _create_books

@pytest.fixture
def borrow_books(session, customer_user, create_books):
    books = create_books(2)
    book = books[0]
    borrowed_book = BorrowedBook(
        user_id=customer_user.id,
        book_id=book.id,
        borrowed_date=datetime.now(),
        returned_date=datetime.now() + timedelta(days=14)
    )
    session.add(borrowed_book)
    session.commit()
    return borrowed_book