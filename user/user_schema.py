import os

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field




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


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    phone_no: str = Field(...)
    email: EmailStr = Field(...)
    verified: bool = Field(default=False)
    link: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "johndoe@databoard.ai",
                "phone_no": "07061046672",
                "link": "www.databoard.ai",
                "verified": False,
            }
        }


class RegistrationResponse(BaseModel):
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
                "phone_no": "07061046672",
                "link": "www.databoard.ai",
                "verified": False,
            }
        }


class UserProfile(BaseModel):
    name: str
    org_type: str
    location: str

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Databoard",
                "org_type": "FinTech",
                "location": "Abuja",
            }
        }


class OrganizationInfo(BaseModel):
    no_employees: str
    no_branches: str
    image: str

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "no_employees": "34",
                "no_branches": "4",
                "image": "Abuja",
            }
        }
