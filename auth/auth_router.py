from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.password_util import PasswordHasher
from oauth.service import create_access_token
from utils.mongo_collections import DATABOARD_COLLECTIONS
from utils.mongo_connect import db

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = await db[DATABOARD_COLLECTIONS.USERS].find_one(
        {"email": user_credentials.username}
    )

    if user and PasswordHasher().verify_password(
        user_credentials.password, user["password"]
    ):
        access_token = create_access_token({"id": user["_id"]})

        """Fetch user cards"""
        tags = await db[DATABOARD_COLLECTIONS.TAGS].find_one(
            {"email": user["email"]}
        )
        tags = [tags]
        return {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Login successful",
            "data": {
                "user": user,
                "access_token": access_token,
                "tags": tags,
            },
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "Error",
                "message": "Invalid Credentials",
                "data": "Error",
            },
        )


@router.post("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user_credentials: OAuth2PasswordBearer = Depends(
        OAuth2PasswordBearer(tokenUrl="token")
    ),
):
    user = await db[DATABOARD_COLLECTIONS.USERS].find_one(
        {"email": user_credentials.email}
    )

    if user and PasswordHasher().verify_password(
        user_credentials.password, user["password"]
    ):
        access_token = create_access_token({"id": user["_id"]})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            detail="Invalid credentials", status_code=status.HTTP_403_FORBIDDEN
        )
