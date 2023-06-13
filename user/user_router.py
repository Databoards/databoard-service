from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from .user_schema import *
from utils.mongo_collections import DATABOARD_COLLECTIONS
from utils.mongo_connect import db

router = APIRouter(tags=["User Routes"])


@router.post("/register")
async def register(user_data: User):
    try:
        user_data = jsonable_encoder(user_data)
        email_exists = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"email": user_data["email"]}
        )
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "Opps! another account exists with this email",
                    "data": "",
                },
            )

        new_org = await db[DATABOARD_COLLECTIONS.USERS].insert_one(user_data)

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
                "message": "Opps! Something went wrong",
                "data": "",
            },
        )


@router.post("/profile")
async def register(profile_data: UserProfile):
    try:
        profile_data = jsonable_encoder(profile_data)
        account_exists = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"email": profile_data["email"]}
        )
        if account_exists:
            if len(profile_data) > 1:
                update_result = await db[DATABOARD_COLLECTIONS.USERS].update_one(
                    {"email": profile_data["email"]},
                    {
                        "$set": {
                            "name": profile_data["name"],
                            "org_type": profile_data["org_type"],
                            "location": profile_data["location"],
                        }
                    },
                )

                if update_result.matched_count == 1:
                    updated_profile = await db[
                        DATABOARD_COLLECTIONS.USERS
                    ].find_one({"email": profile_data["email"]})
                    if (updated_profile) is not None:
                        return {
                            "status_code": status.HTTP_200_OK,
                            "status": "success",
                            "message": "Details added successfully",
                            "data": updated_profile,
                        }
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                                "status": "error",
                                "message": "Could not find this account in the database",
                                "data": "",
                            },
                        )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={
                            "status": "error",
                            "message": "Something went wrong",
                            "data": "",
                        },
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "status": "error",
                        "message": "Something went wrong",
                        "data": "",
                    },
                )

    except Exception:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Opps! Something went wrong",
                "data": "",
            },
        )


@router.post("/info")
async def register(profile_data: OrganizationInfo):
    try:
        profile_data = jsonable_encoder(profile_data)
        account_exists = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"email": profile_data["email"]}
        )
        if account_exists:
            if len(profile_data) > 1:
                update_result = await db[DATABOARD_COLLECTIONS.USERS].update_one(
                    {"email": profile_data["email"]},
                    {
                        "$set": {
                            "no_employees": profile_data["no_employees"],
                            "no_branches": profile_data["no_branches"],
                            "image": profile_data["image"],
                        }
                    },
                )

                if update_result.matched_count == 1:
                    updated_profile = await db[
                        DATABOARD_COLLECTIONS.USERS
                    ].find_one({"email": profile_data["email"]})
                    if (updated_profile) is not None:
                        return {
                            "status_code": status.HTTP_200_OK,
                            "status": "success",
                            "message": "Details added successfully",
                            "data": updated_profile,
                        }
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                                "status": "error",
                                "message": "Could not find this account in the database",
                                "data": "",
                            },
                        )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={
                            "status": "error",
                            "message": "Something went wrong",
                            "data": "",
                        },
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "status": "error",
                        "message": "Something went wrong",
                        "data": "",
                    },
                )

    except Exception:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Opps! Something went wrong",
                "data": "",
            },
        )
