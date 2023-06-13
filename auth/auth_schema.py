import os

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# TODO : Create a separate file to store collection names

# load env
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.clocker


# MongoDb Uses BSON while FastAPI Uses JSON
# Hence to work with fastapi, we need to convert the BSON into JSON
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, filed_schema):
        filed_schema.update(type="string")


class TokenData(BaseModel):
    id: str


class NewPassword(BaseModel):
    new_password: str


class LoginCredentials(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jsduna@gmail.com",
                "password ": "my_pin",
            }
        }
