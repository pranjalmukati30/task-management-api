from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users")

class User(BaseModel):
    name : str
    email : str

class UserUpdate(BaseModel):
    name : str | None = None
    email : str | None = None

users = [
    {"id": 1, "name": "Pranjal", "email": "pranjal@gmail.com"},
    {"id": 2, "name": "Rahul", "email": "rahul@gmail.com"},
]


@router.get("",tags=["Users"])
def all_users():
    return users

@router.get("/{user_id}",tags=["Users"])
def user(user_id:int):
    for user in users:
        if user.get("id") == user_id:
            return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.post("",tags=["Users"])
def create_user(user:User):
    new_id = max(user["id"] for user in users) + 1
    new_user = {
        "id" : new_id,
        "name" : user.name,
        "email" : user.email
    }
    users.append(new_user)

    return new_user

@router.put("/{user_id}",tags=["Users"])
def update_user(user_id:int, user:UserUpdate):
    for existing_user in users:
        if existing_user["id"] == user_id:
            updated_data = user.model_dump(exclude_unset=True)
            existing_user.update(updated_data)
            return existing_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@router.delete("/{user_id}",tags=["Users"])
def delete_user(user_id:int):
    for index,user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return {"message" : "User Deleted Successfully"}

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

