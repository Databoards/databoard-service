from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from utils.mongo_collections import DATABOARD_COLLECTIONS
from utils.mongo_connect import db
from utils.password_util import PasswordHasher

from .user_schema import *

router = APIRouter(tags=["User Routes"])


@router.post("/register")
async def register(user_data: User):
    try:
        user_data = jsonable_encoder(user_data)

        email_exists = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"email": user_data["email"]}
        )

        if email_exists:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "Opps! another account exists with this email",
                    "data": "",
                },
            )

        user_data["org_password"] = PasswordHasher.get_password_hash(
            user_data["org_password"]
        )

        new_org = await db[DATABOARD_COLLECTIONS.USERS].insert_one(user_data)

        otp = "123456"

        """send otp tp user's phone"""
        # send_otp(otp, user_info["phone_no"])

        ""
        add_otp_to_user_account = await db[DATABOARD_COLLECTIONS.USERS].update_one(
            {"email": user_data["email"]}, {"$set": {"otp": otp}}
        )

        created_org = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"_id": new_org.inserted_id}
        )
        return {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Registration successful",
            "data": created_org,
        }

    except Exception:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Opps! something went wrong",
                "data": "",
            },
        )


@router.post("/verify-account")
async def verify_otp(otp_info: UserVerification):
    try:
        otp_info = jsonable_encoder(otp_info)

        user = db[DATABOARD_COLLECTIONS.USERS].find_one(otp_info)
        if not user:
            return HTTPException(
                status_code=400,
                detail={"status": "Error", "message": "User not found", "data": ""},
            )

        # Update the user's status to "email_verified"
        db[DATABOARD_COLLECTIONS.USERS].update_one(
            {
                "email": otp_info["email"],
            },
            {"$set": {"status": True}},
        )

        return {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Account verification was successful",
            "data": "",
        }

    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "Error",
                "message": "Something went wrong",
                "data": e.detail,
            },
        )
