from fastapi import APIRouter, HTTPException, status

from oauth.service import create_access_token, get_current_user
from utils.mongo_collections import CLOCKER_COLLECTIONS
from utils.utils import PasswordHasher

from .schema import NewPassword, PasswordReset, db

router = APIRouter(
    prefix="/password",
    tags=["Password reset"],
)


@router.post("", response_description="Reset Password Request")
async def reset_request(user_email: PasswordReset):
    user = await db[CLOCKER_COLLECTIONS.USERS].find_one({"email": user_email.email})

    if user is not None:
        token = create_access_token({"_id": user["_id"]})
        {"status_code": status.OK, "detail": f"OTP sent"}

    else:
        raise HTTPException(
            detail="Invalid email", status_code=status.HTTP_404_NOT_FOUND
        )


@router.put("", response_description="Reset Password")
async def reset_password(token: str, new_password: NewPassword):
    request_data = {k: v for k, v in new_password.dict().items() if v is not None}

    request_data["password"] = PasswordHasher.get_password_hash(
        request_data["password"]
    )

    if len(request_data) > 1:
        user = await get_current_user(token)
        update_result = await db[CLOCKER_COLLECTIONS.USERS].update_one(
            {"_id": user["_id"]}, {"$set": request_data}
        )

        if update_result.modified_count == 1:
            update_user = await db[CLOCKER_COLLECTIONS.USERS].find_one(
                {"_id": user["_id"]}
            )

            if (update_user) is not None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "detail": f"Password rest successful",
                }

    existing_user = await db[CLOCKER_COLLECTIONS.USERS].find_one({"_id": user["_id"]})

    if (existing_user) is not None:
        return existing_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User information not found"
    )
