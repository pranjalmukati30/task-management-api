from fastapi import FastAPI
from app.routers import users,projects,tasks,users_v2


app = FastAPI()
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(users_v2.router, prefix="/api/v2")



@app.get("/")
def home():
    return {
        "message" : "Task Management API"
    }