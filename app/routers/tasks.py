from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/tasks")

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


tasks = [{"id": 1,"title": "Design API structure","description": "Plan the endpoints and overall API structure","status": "pending","priority": "high","project_id": 1,"assigned_to": 2},
    {"id": 2,"title": "Implement User Authentication","description": "Add login and authentication functionality","status": "in_progress","priority": "high","project_id": 1,"assigned_to": 1},
    {"id": 3,"title": "Create Product APIs","description": "Build APIs for products and categories","status": "pending","priority": "medium","project_id": 2,"assigned_to": 2},
    {"id": 4,"title": "Create Student Module","description": "Implement student management functionality","status": "completed","priority": "low","project_id": 3,"assigned_to": 1}
]


@router.get("",tags=["Tasks"])
def all_tasks():
    return tasks

@router.get("/{task_id}",tags=["Tasks"])
def task(task_id:int):
    for task in tasks:
        if task.get("id") == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.post("",tags=["Tasks"])
def create_task(task:Task):
    new_id = max(task["id"] for task in tasks) + 1
    new_task = {
        "id" : new_id,
        "title" : task.title,
        "description" : task.description,
        "status" : task.status,
        "priority" : task.priority,
        "project_id" : task.project_id,
        "assigned_to" : task.assigned_to
    }
    tasks.append(new_task)
    return new_task

@router.put("/{task_id}",tags=["Tasks"])
def update_task(task:TaskUpdate, task_id:int):
    for existing_task in tasks:
        if existing_task["id"] == task_id:
            updated_task = task.model_dump(exclude_unset=True)
            existing_task.update(updated_task)
            return existing_task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.delete("/{task_id}",tags=["Tasks"])
def delete_task(task_id:int):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return {"message" : "Task deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
