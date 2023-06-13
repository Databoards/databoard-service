import os

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, EmailStr, Field




class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            return {
                "status": "Error",
                "message": "Validation Error, All fields are required",
                "data": "",
            }
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, filed_schema):
        filed_schema.update(type="string")


class Tag(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str = Field(...)
    tag_name: EmailStr = Field(...)
    start_date: str = Field(...)
    end_date: EmailStr = Field(...)
    start_time: str = Field(...)
    end_time: EmailStr = Field(...)
    qr_link: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "johndoe@databoard.ai",
                "tag_name": "07061046672",
                "start_date": "12:02:2023",
                "start_time": "05:23",
                "end_date": "12:02:2023",
                "end_time": "05:23",
                "qr_link": "www.cloudinary.com",
            }
        }


class TagResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    phone: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "johndoe@databoard.ai",
                "tag_name": "07061046672",
                "start_date": "12:02:2023",
                "start_time": "05:23",
                "end_date": "12:02:2023",
                "end_time": "05:23",
                "qr_link": "www.cloudinary.com",
            }
        }



