from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name : str
    email : str

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