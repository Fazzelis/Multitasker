from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
import secrets
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from crud import *


hashing_password = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()


def get_password_hash(password: str):
    return hashing_password.hash(password)


def match_hash(password: str, password_hash: str) -> bool:
    return hashing_password.verify(password, password_hash)


def generate_and_send_verify_code(to_email: str) -> str:
    # Подключение к серверу ддя отправки сообщения на почту
    server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("PORT")))
    server.starttls()
    server.ehlo()

    # Вход в аккаунт, с которого будем отправлять сообщение
    from_email = os.getenv("EMAIL_LOGIN")
    server.login(from_email, os.getenv("EMAIL_PASSWORD"))
    reset_token = secrets.token_urlsafe(6)

    # Заполнение сообщения
    subject = "Восстановление пароля"
    body = f"Код восстановления: {reset_token}"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = from_email
    msg["To"] = to_email

    # Отправка сообщения
    server.sendmail(from_email, to_email, msg.as_string())

    server.quit()
    return get_password_hash(reset_token)


def save_avatar(email: str, avatar) -> str:
    filename = f"{email}.{avatar.filename.split('.')[-1]}"
    file_path = os.path.join("src", "users_avatar", filename)
    with open(file_path, "wb") as new_file:
        new_file.write(avatar.file.read())
    return file_path


def encode_jwt(
        payload: dict,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM"),
        expire_minutes: int = 15):
    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=expire_minutes)
    payload.update(
        exp=expire_time.timestamp(),
        iat=now.timestamp()
    )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(token, public_key: str = os.getenv("PUBLIC_KEY"), algorithm: str = os.getenv("ALGORITHM")) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
        leeway=10
    )
    return decoded
