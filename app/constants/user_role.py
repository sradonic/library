import enum


class UserRole(str, enum.Enum):
    admin = 'admin'
    customer = 'customer'
    librarian = 'librarian'
