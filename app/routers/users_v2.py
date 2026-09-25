from fastapi import APIRouter, HTTPException
from app.routers.users import users

router = APIRouter(prefix="/users")

@router.get("/{user_id}",tags=["Users"])
def get_user(user_id:int):
    for user in users:
        if user.get("id") == user_id:
            return {
                "id": user["id"],
                "full_name": user["name"],
                "email": user["email"]
            }
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")