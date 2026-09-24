from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name : str
    email : str

class UserUpdate(BaseModel):
    name : str | None = None
    email : str | None = None

app = FastAPI()

users = [
    {"id": 1, "name": "Pranjal", "email": "pranjal@gmail.com"},
    {"id": 2, "name": "Rahul", "email": "rahul@gmail.com"},
]

@app.get("/")
def home():
    return {
        "message" : "Task Management API"
    }

@app.get("/users",tags=["Users"])
def all_users():
    return users

@app.get("/users/{user_id}",tags=["Users"])
def user(user_id:int):
    for user in users:
        if user.get("id") == user_id:
            return user
    return {"error" : "User not found"}

@app.post("/users",tags=["Users"])
def create_user(user:User):
    new_user = {
        "id" : len(users) +1,
        "name" : user.name,
        "email" : user.email
    }
    users.append(new_user)

    return new_user

@app.delete("/users/{user_id}",tags=["Users"])
def delete_user(user_id:int):
    for index,user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return {"messgae" : "User Deleted Successfully"}

    return {"error" : "User not found."}

@app.put("/users/{user_id}",tags=["Users"])
def update_user(user_id:int, user:UserUpdate):
    for existing_user in users:
        if existing_user["id"] == user_id:
            updated_data = user.model_dump(exclude_unset=True)
            existing_user.update(updated_data)
            # existing_user["name"] = user.name
            # existing_user["email"] = user.email

            return existing_user,"Updated"
    return {"error": "User not found"}