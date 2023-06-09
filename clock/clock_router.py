import uuid
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime,date
from oauth import service
from user.user_schema import User
from utils.mongo_collections import DATABOARD_COLLECTIONS,CLOCKER_COLLECTIONS
from utils.mongo_connect import db



router = APIRouter(tags=["Clock Routes"], prefix="/clocks")

@router.get("/fetch_tag_clocks/{tag_id}")
async def fetch_tag_clocks(tag_id: str, current_user: User = Depends(service.get_current_user)):
    try:
        tag_id_str = str(tag_id)  # Convert tag_id to a string

        clocks = await db[DATABOARD_COLLECTIONS.TAGS].find_one({"org_id": current_user.get("_id"), "tag_code": tag_id_str}, projection={"clocks": True})
        clocks=clocks.get('clocks')
        if clocks:
            user_ids = [clock.get("user_id") for clock in clocks]
            users = await db[CLOCKER_COLLECTIONS.USERS].find({"_id": {"$in": user_ids}}).to_list(length=None)

            user_map = {str(user["_id"]): user for user in users}

            clocks_with_users = []
            for clock in clocks:
                timestamp = datetime.fromisoformat(clock.get('time'))
                time = timestamp.time().strftime('%H:%M:%S')
                date = timestamp.date()
                user_id = clock.get("user_id")
                user_info = user_map.get(user_id)
                dob=datetime.strptime(user_info.get("dob"), "%Y-%m-%d %H:%M:%S.%f").date()
                today = date.today()
                if user_info:
                    clock.update({
                        "tag_id": tag_id_str,
                        "email": user_info.get("email"),
                        "fname": user_info.get("first_name"),
                        "lname": user_info.get("last_name"),
                        "gender": user_info.get("gender"),
                        "age": user_info.get("age"),
                        "dob":today.year - dob.year,
                        "time":time,
                        "date":date,
                        "rating":5,
                    })

                clocks_with_users.append(clock)
            return {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "message": "Clocks successfully retrieved.",
                "data": clocks_with_users,
            }
        else:
            return {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "message": "Clocks successfully retrieved but empty.",
                "data": [],
            }
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Oops! Something went wrong",
                "data": f"This is the bug bro {e}",
            },
        )