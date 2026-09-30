from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task

router = APIRouter(prefix="/tasks")


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    project_id: int
    assigned_to: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    project_id: int | None = None
    assigned_to: int | None = None


@router.get("", tags=["Tasks"])
def all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@router.get("/{task_id}", tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task

@router.post("", tags=["Tasks"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        project_id=task.project_id,
        assigned_to=task.assigned_to
    )

    db.add(new_task)
    db.commit()

    return new_task

@router.put("/{task_id}", tags=["Tasks"])
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    updated_data = task.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(existing_task, field, value)

    db.commit()

    return existing_task


@router.delete("/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": f"Task {task_id} deleted successfully"
    }