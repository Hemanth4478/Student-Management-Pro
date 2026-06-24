from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
    marks: int

class UserCreate(BaseModel):
    username:str
    password:str