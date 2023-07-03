import os

import motor.motor_asyncio
from dotenv import load_dotenv

# load env
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.clocker
