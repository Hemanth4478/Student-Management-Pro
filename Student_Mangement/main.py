from fastapi import FastAPI
from database.db import create_tables
from routes.auth import router as auth_router
from routes.students import router as student_router

app = FastAPI()

create_tables()

app.include_router(auth_router)
app.include_router(student_router)
@app.get("/")
def home():
    return {"message": "Student Management Pro"}