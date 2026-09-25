from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.routers import users
from app.routers import projects
from app.routers import tasks


app = FastAPI()
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")



@app.get("/")
def home():
    return {
        "message" : "Task Management API"
    }
