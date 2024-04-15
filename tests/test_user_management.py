import pytest
from fastapi.testclient import TestClient
from app.database.database import get_db
from app.main import app
from app.models import User

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_create_user_as_admin(client, admin_user, generate_token, roles):
    access_token = generate_token(admin_user)

    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "name": "New User",
            "email": "newuser@example.com",
            "password": "NewSecure123",
            "role": "customer"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_create_user_as_librarian(client, librarian_user, generate_token, roles):
    access_token = generate_token(librarian_user)

    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "name": "New User",
            "email": "newuser@example.com",
            "password": "NewSecure123",
            "role": "customer"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

def test_create_user_as_non_admin(client, customer_user, generate_token):
    access_token = generate_token(customer_user)

    response = client.post("/users/", json={
        "username": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "password": "Password123",
        "role": "customer"
    }, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403


def test_edit_user_details_as_admin(client, admin_user, generate_token, make_customer):
    access_token = generate_token(admin_user)

    response = client.put(
        f"/users/{make_customer.id}",
        json={
            "username": "updatedUser",
            "email": "updated@example.com",
            "name": "Updated User"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_edit_user_details_as_non_admin(client, customer_user, generate_token, make_customer):
    access_token = generate_token(customer_user)

    response = client.put(
        f"/users/{make_customer.id}",
        json={
            "username": "updatedUser",
            "email": "updated@example.com",
            "name": "Updated User"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 403


def test_list_users_as_admin(client, admin_user, generate_token, make_customer, session):
    access_token = generate_token(admin_user)

    user_in_db = session.query(User).filter_by(id=make_customer.id).first()
    assert user_in_db is not None, "Role should be created."

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    response_data = response.json()

    customer_found = any(user['username'] == make_customer.username for user in response_data)

    assert customer_found, "Customer user should be in the list"

    for user in response_data:
        if user['username'] == make_customer.username:
            assert user['email'] == make_customer.email, "existing@example.com"
            assert user['name'] == make_customer.name, "Existing User"


def test_list_users_as_librarian(client, librarian_user, admin_user, generate_token, make_customer, session):
    access_token = generate_token(librarian_user)

    user_in_db = session.query(User).filter_by(id=make_customer.id).first()
    assert user_in_db is not None, "Role should be created."

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    response_data = response.json()

    customer_found = any(user['username'] == make_customer.username for user in response_data)

    assert customer_found, "Customer user should be in the list"

    for user in response_data:
        if user['username'] == make_customer.username:
            assert  user['email'] == make_customer.email, "existing@example.com"
            assert  user['name'] == make_customer.name, "Existing User"

    for user in response_data:
        if user['id'] == 1:
            assert not user['email'] == admin_user.email, "admin@example.com"
            assert not user['name'] == admin_user.name, "Admin User"


def test_list_users_as_customer(client, customer_user, generate_token, make_customer, session):
    access_token = generate_token(customer_user)

    user_in_db = session.query(User).filter_by(id=make_customer.id).first()
    assert user_in_db is not None, "Role should be created."

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
