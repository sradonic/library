from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.book import Book
from faker import Faker
import random

faker = Faker()

def create_random_book():
    return Book(
        title=faker.catch_phrase(),
        author=faker.name(),
        description=faker.text(max_nb_chars=200),  # Generates a random text up to 200 characters
        quantity=random.randint(1, 5)  # Random quantity between 1 and 100
    )

def add_books_to_db(number_of_books: int, db: Session = SessionLocal()):
    for _ in range(number_of_books):
        db_book = create_random_book()
        db.add(db_book)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    num_books_to_add = 2
    add_books_to_db(num_books_to_add, db)
