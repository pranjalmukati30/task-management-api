from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/users")

class UserCreate(BaseModel):
    name : str
    email : str

class UserUpdate(BaseModel):
    name : str | None = None
    email : str | None = None

class UserResponse(BaseModel):
    id : int
    name : str
    # age : int | None = None


@router.get("",tags=["Users"])
def all_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}",tags=["Users"])
def get_user(user_id:int, db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return user


@router.post("",tags=["Users"])
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    new_user = User(
        name = user.name,
        email = user.email,
    )
    db.add(new_user)
    db.commit()
    return new_user


@router.put("/{user_id}",tags=["Users"])
def update_user(user_id:int, user:UserUpdate, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    updated_data = user.model_dump(exclude_unset=True)

    # Update the existing SQLAlchemy object
    for field, value in updated_data.items():
        setattr(existing_user, field, value)

    # Save changes to database
    db.commit()
    return existing_user


@router.delete("/{user_id}",tags=["Users"])
def delete_user(user_id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    db.delete(user)
    db.commit()
    return {"message" : f"User {user_id} deleted successfully"}