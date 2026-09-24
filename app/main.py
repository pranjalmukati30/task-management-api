from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Users Pydantic model
class User(BaseModel):
    name : str
    email : str

class UserUpdate(BaseModel):
    name : str | None = None
    email : str | None = None


# Projects Pydantic model
class Project(BaseModel):
    name : str
    description : str
    owner_id : int

class ProjectUpdate(BaseModel):
    name : str | None = None
    description : str | None = None

app = FastAPI()

users = [
    {"id": 1, "name": "Pranjal", "email": "pranjal@gmail.com"},
    {"id": 2, "name": "Rahul", "email": "rahul@gmail.com"},
]

projects = [
    {"id": 1,"name": "Task Management API","description": "Backend API for managing projects and tasks","owner_id": 1},
    {"id": 2,"name": "E-Commerce Backend","description": "Backend system for an online shopping platform","owner_id": 2},
    {"id": 3,"name": "College Management System","description": "System for managing students, courses and faculty","owner_id": 1}
]

@app.get("/")
def home():
    return {
        "message" : "Task Management API"
    }

# user endpoints
@app.get("/users",tags=["Users"])
def all_users():
    return users

@app.get("/users/{user_id}",tags=["Users"])
def user(user_id:int):
    for user in users:
        if user.get("id") == user_id:
            return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


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
            return {"message" : "User Deleted Successfully"}

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@app.put("/users/{user_id}",tags=["Users"])
def update_user(user_id:int, user:UserUpdate):
    for existing_user in users:
        if existing_user["id"] == user_id:
            updated_data = user.model_dump(exclude_unset=True)
            existing_user.update(updated_data)
            return existing_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

# project endpoints
@app.get("/projects",tags=["Projects"])
def all_projects():
    return projects

@app.get("/projects/{project_id}",tags=["Projects"])
def project(project_id:int):
    for project in projects:
        if project.get("id") == project_id:
            return project
    raise HTTPException(status_code=404,detail=f"Project {project_id} not found")

@app.post("/projects",tags=["Projects"])
def create_project(project:Project):
    new_project = {
        "id" : len(projects)+1,
        "name" : project.name,
        "description" : project.description,
        "owner_id" : project.owner_id
    }
    projects.append(new_project)
    return new_project
    

@app.put("/projects/{project_id}",tags=["Projects"])
def update_project(project:ProjectUpdate, project_id:int):
    for existing_project in projects:
        if existing_project["id"] == project_id:
            updated_project = project.model_dump(exclude_unset=True)
            existing_project.update(updated_project)
            return existing_project
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

@app.delete("/projects/{project_id}",tags=["Projects"])
def delete_project(project_id:int):
    for index,project in enumerate(projects):
        if project["id"] == project_id:
            projects.pop(index)
            return {"message" : "Project deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
