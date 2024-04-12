import pytest
from app.schemas.user import UserCreate


def test_user_create_invalid_email():
    with pytest.raises(ValueError):
        UserCreate(username="testuser", name="Test User", email='testuom', password='123', role='customer')

def test_user_create_missing_parameter():
    with pytest.raises(ValueError):
        UserCreate(username="testuser", name="Test User", password='123', role='customer')

def test_password_complexity():
    with pytest.raises(ValueError):
        UserCreate(username = "testuser", name="Test User", email='testuser@email.com', password='123', role='customer')