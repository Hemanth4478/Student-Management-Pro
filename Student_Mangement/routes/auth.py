from fastapi import APIRouter
import sqlite3
from utilites.auth_utilites import create_acces_token
from utilites.security import  hash_password,verify_password
from fastapi import HTTPException
router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str):
    print("PASSWORD:", password)
    print("TYPE:", type(password))
    print("LENGTH:", len(password))

    hashed_password = hash_password(password)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    return {"message": "User created"}


@router.post("/login")
def login(username: str, password: str):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? ",
        (username,)
    )   

    user = cursor.fetchone()
    
    

    if not verify_password(password,user[2]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    token=create_acces_token({"username": username})

    conn.close()

    if user:
        return {"message": "Login successful","access_token": token,"token_type": "bearer"}

    else:
        return {"message": "Invalid username or password"}