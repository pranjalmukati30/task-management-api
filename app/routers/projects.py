from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router=APIRouter(prefix="/projects")

class Project(BaseModel):
    name : str
    description : str
    owner_id : int

class ProjectUpdate(BaseModel):
    name : str | None = None
    description : str | None = None


projects = [
    {"id": 1,"name": "Task Management API","description": "Backend API for managing projects and tasks","owner_id": 1},
    {"id": 2,"name": "E-Commerce Backend","description": "Backend system for an online shopping platform","owner_id": 2},
    {"id": 3,"name": "College Management System","description": "System for managing students, courses and faculty","owner_id": 1}
]


@router.get("",tags=["Projects"])
def all_projects():
    return projects

@router.get("/{project_id}",tags=["Projects"])
def project(project_id:int):
    for project in projects:
        if project.get("id") == project_id:
            return project
    raise HTTPException(status_code=404,detail=f"Project {project_id} not found")

@router.post("",tags=["Projects"])
def create_project(project:Project):
    new_id = max(project["id"] for project in projects) + 1
    new_project = {
        "id" : new_id,
        "name" : project.name,
        "description" : project.description,
        "owner_id" : project.owner_id
    }
    projects.routerend(new_project)
    return new_project

@router.put("/{project_id}",tags=["Projects"])
def update_project(project:ProjectUpdate, project_id:int):
    for existing_project in projects:
        if existing_project["id"] == project_id:
            updated_project = project.model_dump(exclude_unset=True)
            existing_project.update(updated_project)
            return existing_project
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

@router.delete("/{project_id}",tags=["Projects"])
def delete_project(project_id:int):
    for index,project in enumerate(projects):
        if project["id"] == project_id:
            projects.pop(index)
            return {"message" : "Project deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

