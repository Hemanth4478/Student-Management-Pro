from fastapi import APIRouter
import sqlite3
from models.student import StudentCreate
from fastapi import HTTPException
from fastapi import Header, HTTPException
from utilites.auth_utilites import verify_token


from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()
router = APIRouter()

@router.get("/profile")
def profile(credentials = Depends(security)):

    token = credentials.credentials
    
    print("TOKEN =", token)

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "success": True,
        "message": "Access granted",
        "user": {
            "username": payload["username"]
        }
    }

# @router.get("/profile")
# def profile(
#     authorization: str = Header(None)
# ):
#     print(authorization)
#     if not authorization:
#         raise HTTPException(
#             status_code=401,
#             detail="Token missing"
#         )

#     token = authorization.split(" ")[1]

#     payload = verify_token(token)

#     if not payload:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid token"
#         )

#     return {
#         "message": "Access granted",
#         "user": payload
#     }



@router.post("/students")
def add_student(students :StudentCreate):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, age, marks) VALUES(?,?,?)",
        (students.name, students.age, students.marks)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Student added successfully",
        "data": {
            "name": students.name,
            "age": students.age,
            "marks": students.marks
        }
    }
    
@router.get("/students")
def get_students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students

@router.get("/students/{name}")
def search_student(name: str):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name=?",
        (name,)
    )

    student = cursor.fetchone()


    conn.close()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "success": True,
        "data": {
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "marks": student[3]
        }
    }
    



@router.put("/students/{id}")
def update_marks(id: int, marks: int):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Check student exists
    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    if not student:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Update marks
    cursor.execute(
        "UPDATE students SET marks=? WHERE id=?",
        (marks, id)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Marks updated successfully"
    }

@router.delete("/students/{id}")
def delete_student(id: int):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "select * FROM students WHERE id=?",
        (id,)
    )
    student=cursor.fetchone()
    if not student:
       conn.close()
       raise HTTPException(status_code=404,details="f {id} not found")
    
    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Deleted"}

@router.get("/student")
def topper_student():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "select name,max(marks) FROM students"
        
    )
    student=cursor.fetchone()
    if not student:
       conn.close()
       raise HTTPException(status_code=404,details=" not found")
    
    

    conn.commit()
    conn.close()

    return { 
            "name":student[0],
            "marks":student[1],
            }


@router.get("/stude")
def avg_student():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "select avg(marks)as total_marks FROM students"
        
    )
    student=cursor.fetchone()
    if not student:
       conn.close()
       raise HTTPException(status_code=404,details=" not found")
    
    

    conn.commit()
    conn.close()

    return { 
            "avg_marks":student[0],
            
            }

@router.get("/fortyplus")
def above_foutystudent():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "select count(*) FROM students where marks >=40"
        
    )
    student=cursor.fetchone()
    if not student:
       conn.close()
       raise HTTPException(status_code=404,details=" no one is there")
    

    conn.commit()
    conn.close()

    return { 
            "count":student[0],
            
            }