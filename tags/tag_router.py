import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from oauth import service
from user.user_schema import User
from utils.mongo_collections import DATABOARD_COLLECTIONS
from utils.mongo_connect import db
from utils.qr_code_generator import destroy_from_cloudinary, generate_qr

from .tag_schema import *

router = APIRouter(tags=["Tag Routes"], prefix="/tags")


@router.post("/create")
async def create_tag(
    tag_data: CreateTag, current_user: User = Depends(service.get_current_user)
):
    try:
        tag_data = jsonable_encoder(tag_data)
        new_tag_code = str(uuid.uuid4())

        tag = Tag(
            org_id=tag_data.get("_id"),
            org_name=current_user.get("org_name"),
            tag_name=tag_data.get("tag_name"),
            tag_type=tag_data.get("tag_type"),
            tag_code=new_tag_code,
            image="https://picsum.photos/640/360",
            qr=generate_qr(
                email=tag_data.get("email"), tag_code=new_tag_code, variant="databoard"
            ),
            start_date=tag_data.get("start_date"),
            end_date=tag_data.get("end_date"),
            start_time=tag_data.get("start_time"),
            end_time=tag_data.get("end_time"),
        )

        tag_exists = await db[DATABOARD_COLLECTIONS.TAGS].find_one(
            {
                "torg_id": current_user.get("_id"),
                "tag_name": tag_data.get("tag_name"),
            }
        )

        if tag_exists is not None:
            destroy_from_cloudinary(pic_type="tag", url=tag_exists["qr"])

            updated_tag = await db[DATABOARD_COLLECTIONS.TAGS].update_one(
                {"email": tag_data.get("email"), "tag_name": tag_data.get("tag_name")},
                {"$set": tag.dict(exclude_unset=True)},
            )
            if updated_tag is not None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "status": "success",
                    "message": "Tag was succesfully created",
                    "data": tag.dict(exclude_unset=True),
                }
            else:
                return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "status": "error",
                        "message": "Could not create personal card",
                        "data": "",
                    },
                )
        else:
            new_personal_card = await db[DATABOARD_COLLECTIONS.TAGS].insert_one(
                tag.dict(exclude_unset=True)
            )

            if new_personal_card is not None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "status": "success",
                    "message": "Tag was succesfully created",
                    "data": tag.dict(exclude_unset=True),
                }
            else:
                return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "status": "error",
                        "message": "Could not create personal card",
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


@router.get("/fetch_all")
async def get_tags(current_user: User = Depends(service.get_current_user)):
    try:
        tags_cursor = db[DATABOARD_COLLECTIONS.TAGS].find(
            {"email": current_user["email"]},
            projection={"_id": False},  # Exclude the ObjectId field
        )
        tags = await tags_cursor.to_list(length=None)  # Convert cursor to list

        if tags:
            return {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "message": "Request was successful",
                "data": jsonable_encoder(tags),
            }
        else:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": "No tags found for your organization",
                    "data": "",
                },
            )
    except Exception as e:
        print(f"The error is here: {str(e)}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": "Something went wrong", "data": ""},
        )


@router.post("/get_single/{tag_id}")
async def get_tag(tag_id: str, current_user: User = Depends(service.get_current_user)):
    try:
        tags = await db[DATABOARD_COLLECTIONS.TAGS].find(
            {"email": current_user["email"], "_id": {tag_id}}
        )
        if tags is not None:
            return {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "message": "Request was successfull",
                "data": jsonable_encoder(tags),
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": "No tags found for your organization",
                    "data": "",
                },
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Something went wrong", "data": ""},
        )


@router.delete("/delete_one/{tag_id}")
async def get_tag(tag_id: str, current_user: User = Depends(service.get_current_user)):
    try:
        result = await db[DATABOARD_COLLECTIONS.TAGS].delete_one(
            {"org_id": current_user["_id"], "_id": {tag_id}}
        )
        if result.deleted_count == 1:
            return {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "message": "Request was successfull",
                "data": "",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": "Unable to delete tag",
                    "data": "",
                },
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Something went wrong", "data": ""},
        )
