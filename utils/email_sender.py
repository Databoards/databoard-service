import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


def send_email(subject: str, body: any, to: str):
    load_dotenv()

    user = os.getenv("GMAIL_ACCOUNT")
    password = os.getenv("GMAIL_PASS")
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"]: to
    msg["from"] = user

    server = smtplib.SMTP("smtp.gmail.com", 465)
    server.starttls()
    server.login(user=user, password=password)
    server.send(msg)
    server.quit()
