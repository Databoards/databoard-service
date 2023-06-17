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
    org_name:str=Field(...)
    org_type: str = Field(...)
    org_location: str = Field(...)
    no_employees: str = Field(...)
    no_branches: str = Field(...)
    email: EmailStr = Field(...)
    org_phone: str = Field(...)
    org_link: str = Field(...)
    org_password: str = Field(...,min=8)
    image: str = Field(...)
    verified: bool = Field(default=False)
    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "org_name": "Databoard",
                "org_type": "ICT",
                "org_location": "Jos",
                "no_employees": "1-4",
                "no_branches": "3",
                "email": "sales@databoard.ai",
                "org_phone": "07061046672",
                "org_link": "www.databoard.ai",
                "org_password": "password",
                "image":"",
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
    email: EmailStr = Field(...)
    org_type: str
    location: str

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Databoard",
                "email":"johndoe@databoard.ai",
                "org_type": "FinTech",
                "location": "Abuja",
            }
        }


class OrganizationInfo(BaseModel):
    email: EmailStr = Field(...)
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
                "email":"johndoe@databoard.ai",
                "no_branches": "4",
                "image": "Abuja",
            }
        }


class UserVerification(BaseModel):
    email: EmailStr = Field(...)
    otp: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "johndoe@databoard.ai",
                "otp": "123456",
            }
        }

