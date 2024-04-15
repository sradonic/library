from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from app.database.database import get_db
from app.main import app


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_admin_can_get_book_by_id(client, admin_user, generate_token, create_books, session):
    books = create_books(1)
    book_id = books[0].id
    access_token = generate_token(admin_user)

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()['id'] == book_id, "The fetched book ID should match the created book ID"


def test_customer_cannot_get_book_by_id(client, customer_user, generate_token, create_books, session):
    books = create_books(1)
    book_id = books[0].id
    access_token = generate_token(customer_user)

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403, "Customer should not be able to fetch book details by ID"


def test_librarian_can_get_books_list(client, librarian_user, generate_token, create_books, session):
    create_books(5)
    access_token = generate_token(librarian_user)

    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['books']) >= 5, "At least five books should be listed"


def test_librarian_view_user_books(client, session, librarian_user, borrow_books, generate_token):
    access_token = generate_token(librarian_user)

    response = client.get(
        f"/books/user/{borrow_books.user_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0, "Librarian should be able to view books borrowed by users"


def test_customer_cannot_view_other_user_books(client, session, customer_user, borrow_books, generate_token):
    access_token = generate_token(customer_user)

    response = client.get(
        f"/books/user/{borrow_books.user_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403, "Customer should not be able to view other users' borrowed books"


def test_customer_can_view_own_borrowed_books(client, customer_user, generate_token, borrow_books):
    access_token = generate_token(customer_user)
    response = client.get(
        "/books/mybooks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1, "Customer should see their borrowed books"


def test_admin_add_book_to_user(client, admin_user, generate_token, create_books, make_customer):
    user = make_customer
    books = create_books(2)
    book = books[1]

    access_token = generate_token(admin_user)
    response = client.post(
        f"/books/user/{user.id}/book/{book.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "id" in response.json(), "Book should be successfully added to the user"


def test_customer_cannot_add_book(client, customer_user, generate_token, create_books):
    books = create_books(3)
    book = books[2]

    access_token = generate_token(customer_user)
    response = client.post(
        f"/books/user/{customer_user.id}/book/{book.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403, "Customer should not be authorized to add books"


def test_admin_delete_borrowed_book(client, admin_user, generate_token, borrow_books):
    access_token = generate_token(admin_user)

    response = client.delete(
        f"/books/borrowed/{borrow_books.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, "Admin should be able to delete a borrowed book"


def test_admin_update_book_return_date(client, admin_user, generate_token, borrow_books):
    new_return_date = datetime.now() + timedelta(days=30)
    access_token = generate_token(admin_user)

    response = client.patch(
        f"/books/borrowed/{borrow_books.id}/return-date/{new_return_date.isoformat()}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, "Admin should be able to update the return date of a borrowed book"
