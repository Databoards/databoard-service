from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from .tag_schema import *
from utils.mongo_collections import DATABOARD_COLLECTIONS
from utils.mongo_connect import db
from user.user_schema import User
from oauth import service


router = APIRouter(tags=["Tag Routes"],prefix="/delete")


@router.post("/create")
async def create_tag(tag_data: Tag):
    try:
        tag_data = jsonable_encoder(tag_data)

        new_tag = await db[DATABOARD_COLLECTIONS.TAGS].insert_one(tag_data)

        created_tag = await db[DATABOARD_COLLECTIONS.USERS].find_one(
            {"_id": new_tag.inserted_id}
        )
        return {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Tag was succesfully created",
            "data": created_tag,
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


@router.post("/fetch_all")
async def get_tags(current_user: User = Depends(service.get_current_user)):
        try:
            tags = await db[DATABOARD_COLLECTIONS.TAGS].find(
                    {"_id": current_user["tag_id"]}
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
                        detail={"status": "error", "message": "No tags found for your organization", "data": ""},
                    )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Something went wrong", "data": ""},
            )

@router.post("/get_single/{tag_id}")
async def get_tag(tag_id:str,current_user: User = Depends(service.get_current_user)):
        try:
            tags = await db[DATABOARD_COLLECTIONS.TAGS].find(
                    {"email": current_user["email"],"_id":{tag_id}}
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
                        detail={"status": "error", "message": "No tags found for your organization", "data": ""},
                    )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Something went wrong", "data": ""},
            )
 
@router.delete("/delete_one/{tag_id}")
async def get_tag(tag_id:str,current_user: User = Depends(service.get_current_user)):
        try:
            result = await db[DATABOARD_COLLECTIONS.TAGS].delete_one(
                    {"email": current_user["email"],"_id":{tag_id}}
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
                        detail={"status": "error", "message": "Unable to delete tag", "data": ""},
                    )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Something went wrong", "data": ""},
            )