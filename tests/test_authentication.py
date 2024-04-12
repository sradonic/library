import os
from pytest_mock import MockerFixture

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "testsecretkey"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"


from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.core.auth.password_security import get_password_hash

client = TestClient(app)


def test_login_successfully_with_mock(mocker: MockerFixture):
    test_user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password=get_password_hash("testpass123"),
        name="Test User"
    )

    mocker.patch(
        "app.core.auth.authentication.get_user",
        return_value=test_user
    )

    mocker.patch(
        "app.core.auth.password_security.verify_password",
        return_value=True
    )

    response = client.post("/token", data={"username": "testuser", "password": "testpass123"})

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_unsuccessfully_with_wrong_credentials(mocker: MockerFixture):
    mocker.patch(
        "app.core.auth.authentication.get_user",
        return_value=None
    )

    mocker.patch(
        "app.core.auth.password_security.verify_password",
        return_value=False
    )

    response = client.post("/token", data={"username": "wronguser", "password": "wrongpassword"})

    assert response.status_code == 401
    assert "access_token" not in response.json()
    assert response.json()["detail"] == "Incorrect username or password"