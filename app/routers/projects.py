from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_db
from app.models import Project
from sqlalchemy.orm import Session

router=APIRouter(prefix="/projects")

class ProjectCreate(BaseModel):
    name : str
    description : str
    owner_id : int

class ProjectUpdate(BaseModel):
    name : str | None = None
    description : str | None = None



@router.get("",tags=["Projects"])
def all_projects(db:Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects


@router.get("/{project_id}",tags=["Projects"])
def get_project(project_id:int, db:Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    return project


@router.post("", tags=["Projects"])
def create_project(project: ProjectCreate,db: Session = Depends(get_db)):
    new_project = Project(name=project.name,description=project.description,owner_id=project.owner_id)

    db.add(new_project)
    db.commit()

    return new_project

@router.put("/{project_id}", tags=["Projects"])
def update_project(project_id: int,project: ProjectUpdate,db: Session = Depends(get_db)):
    existing_project = (db.query(Project).filter(Project.id == project_id).first())

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} not found"
        )

    updated_data = project.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(existing_project, field, value)

    db.commit()

    return existing_project


@router.delete("/{project_id}", tags=["Projects"])
def delete_project(project_id: int,db: Session = Depends(get_db)):
    project = (db.query(Project).filter(Project.id == project_id).first())

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": f"Project {project_id} deleted successfully"
    }