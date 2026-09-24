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


# Tasks Pydantic model
class Task(BaseModel):
    title : str
    description : str
    status : str
    priority : str
    project_id : int
    assigned_to : int

class TaskUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    status : str | None = None
    priority : str | None = None
    project_id : int | None = None
    assigned_to : int | None = None

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

tasks = [{"id": 1,"title": "Design API structure","description": "Plan the endpoints and overall API structure","status": "pending","priority": "high","project_id": 1,"assigned_to": 2},
    {"id": 2,"title": "Implement User Authentication","description": "Add login and authentication functionality","status": "in_progress","priority": "high","project_id": 1,"assigned_to": 1},
    {"id": 3,"title": "Create Product APIs","description": "Build APIs for products and categories","status": "pending","priority": "medium","project_id": 2,"assigned_to": 2},
    {"id": 4,"title": "Create Student Module","description": "Implement student management functionality","status": "completed","priority": "low","project_id": 3,"assigned_to": 1}
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


# task endpoints
@app.get("/tasks",tags=["Tasks"])
def all_tasks():
    return tasks

@app.get("/tasks/{task_id}",tags=["Tasks"])
def task(task_id:int):
    for task in tasks:
        if task.get("id") == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks",tags=["Tasks"])
def create_task(task:Task):
    new_task = {
        "id" : len(tasks)+1,
        "title" : task.title,
        "description" : task.description,
        "status" : task.status,
        "priority" : task.priority,
        "project_id" : task.project_id,
        "assigned_to" : task.assigned_to
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}",tags=["Tasks"])
def update_task(task:TaskUpdate, task_id:int):
    for existing_task in tasks:
        if existing_task["id"] == task_id:
            updated_task = task.model_dump(exclude_unset=True)
            existing_task.update(updated_task)
            return existing_task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}",tags=["Tasks"])
def delete_task(task_id:int):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return {"message" : "Task deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
