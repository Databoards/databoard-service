import os

from dotenv import load_dotenv
from vonage import Client, Sms

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")

client = Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms = Sms(client)


def send_otp(otp: str, phone: str):
    responseData = sms.send_message(
        {
            "from": "Cloker",
            "to": f"{phone}",
            "text": f"Your verification code is {otp}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        return "Message sent successfully."
    else:
        return f"Message failed with error: {responseData['messages'][0]['error-text']}"
