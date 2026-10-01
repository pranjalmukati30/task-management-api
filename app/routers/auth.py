from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import verify_password

router = APIRouter(prefix="/auth")

class LoginRequest(BaseModel):
    email : EmailStr
    password : str

@router.post("/login",tags=["Auth"])
def login(login_data:LoginRequest, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "message" : "Login successful",
        "user_id" : user.id
    }
