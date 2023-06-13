import random

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from utils import otp_util

from .schema import *

router = APIRouter(
    prefix="/otp",
    tags=["OTP Routes"],
)


@router.post("/send_otp", response_description="Send OTP")
async def send_otp(user_phone: SendOTPData):
    otp_util.random(6)
    try:
        user_phone = jsonable_encoder(user_phone)

        return {"status_code": status.HTTP_200_OK, "detail": f"OTP sent"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/verify_otp", response_description="Send OTP")
async def verify_otp(user_phone: str, otp: str, email: str):
    random.randint(1000, 9999)
    try:
        user_phone = jsonable_encoder(user_phone)

        return {"status_code": status.HTTP_200_OK, "detail": f"OTP Verified"}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
