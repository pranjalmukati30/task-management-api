from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.routers import users
from app.routers import projects
from app.routers import tasks


app = FastAPI()
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)



@app.get("/")
def home():
    return {
        "message" : "Task Management API"
    }
