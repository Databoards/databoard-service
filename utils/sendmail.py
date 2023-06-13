import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

# for more info check https://sabuhish.github.io/fastapi-mail/
# TODO : I am yet to define the values in the dotenv file

load_dotenv()


class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    # 587 for google
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    # smtp.gmail.com for google
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")


config = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="api/utils/email_templates",
)


async def send_registration_mail(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject, recipients=[email_to], template_body=body, subtype="html"
    )

    fm = FastMail(config)

    await fm.send_message(message=message, template_name="reg_email.html")


async def send_password_reset_mail(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject, recipients=[email_to], template_body=body, subtype="html"
    )

    fm = FastMail(config)

    await fm.send_message(message=message, template_name="password_reset_email.html")
