import os
from datetime import datetime, timedelta
from typing import Dict

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from utils.mongo_collections import DATABOARD_COLLECTIONS

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.clocker

oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    id: str


def create_access_token(payload: Dict):
    to_encode = payload.copy()

    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expiration_time})

    jw_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jw_token


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("id")
        if not id:
            raise credential_exception
        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception


async def get_current_user(token: str = Depends(oauth_schema)):
    credentail_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "token_expired",
            "message": "Your session is expired",
            "data": "",
        },
    )
    current_user_id = verify_access_token(token, credentail_exception).id

    current_user = await db[DATABOARD_COLLECTIONS.USERS].find_one(
        {"_id": current_user_id}
    )

    return current_user
