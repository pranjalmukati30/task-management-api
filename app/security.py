from pwdlib import PasswordHash
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(password : str, hashed_password : str) -> bool:
    return password_hash.verify(password,hashed_password)



load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def create_acess_token(user_id:int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# print(create_acess_token(5))

# print("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1In0.f9JN4-atFtST5SzfEuIED4Do6JwjpAux-ROzFBd_1O0" == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1In0.f9JN4-atFtST5SzfEuIED4Do6JwjpAux-ROzFBd_1O0")
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1In0.f9JN4-atFtST5SzfEuIED4Do6JwjpAux-ROzFBd_1O0
# password = "hello123"
# print("Password : ",password)
# hashed = hash_password(password)
# print("\nIt is hashed password : ",hashed,"\n")

# print(verify_password("hello123",hashed))

# print(verify_password("hello",hashed))
