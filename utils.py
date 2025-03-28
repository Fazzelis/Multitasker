from passlib.context import CryptContext
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
import secrets


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
