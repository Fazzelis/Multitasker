from passlib.context import CryptContext


hashing_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return hashing_password.hash(password)
