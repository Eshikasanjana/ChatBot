# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from typing import List, Optional, Annotated
# from Backend import models
# from Backend.database import engine, SessionLocal
# from sqlalchemy.orm import Session

# app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

# class StudentCreate(BaseModel):
#     name:     str
#     grade:    int         
#     subjects: List[str]
#     email:    Optional[str] = None

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# db_dependency = Annotated[Session, Depends(get_db)]


# # GET single student by ID 
# @app.get("/students/{student_id}")
# async def read_student(student_id: int, db: db_dependency):
#     student = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return student


# # GET all students
# @app.get("/students/")
# async def read_all_students(db: db_dependency):
#     return db.query(models.Student).all()


# # GET student by name (used by chatbot)
# @app.get("/students/search/")
# async def search_student_by_name(name: str, db: db_dependency):
#     student = db.query(models.Student).filter(
#         models.Student.name.ilike(f"%{name}%")
#     ).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return student

# # # GET student by ID (used by chatbot)
# # @app.get("/students/search/")
# # async def search_student_by_id(id: int, db: db_dependency):
# #     student = db.query(models.Student).filter(
# #         models.Student.id == id
# #     ).first()
# #     if not student:
# #         raise HTTPException(status_code=404, detail="Student not found")
# #     return student

# # POST register new student
# @app.post("/students/")
# async def register_student(student: StudentCreate, db: db_dependency):
#     db_student = models.Student(
#         name=student.name,
#         grade=student.grade,
#         subjects=student.subjects,
#         email=student.email,
#     )
#     db.add(db_student)
#     db.commit()
#     db.refresh(db_student)
#     return {"message": "Student profile saved!", "student_id": db_student.id}
    
# # ── PUT update student by ID ──────────────────────────────────
# @app.put("/students/{student_id}")
# async def update_student(student_id: int, student: StudentCreate, db: db_dependency):
#     db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not db_student:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     db_student.name = student.name
#     db_student.grade = student.grade
#     db_student.subjects = student.subjects
#     db_student.email = student.email

#     db.commit()
#     db.refresh(db_student)
#     return {"message": "Student updated!", "student": db_student}

# # ── DELETE student by ID ──────────────────────────────────────
# @app.delete("/students/{student_id}")
# async def delete_student(student_id: int, db: db_dependency):
#     db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not db_student:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     db.delete(db_student)
#     db.commit()
#     return {"message": "Student deleted!", "student_id": student_id}

from mcp.server.fastmcp import FastMCP
import json
import pandas as pd

mcp = FastMCP("StudentAssistance")

@mcp.tool()
def get_student_info(name: str):
    """Search for a student in the JSON database by name."""
    with open("data/students.json", "r") as f:
        students = json.load(f)
    
    for s in students:
        if name.lower() in s["name"].lower():
            return s
    return "Student not found."

@mcp.tool()
def read_student_spreadsheet(file_path: str):
    """Reads the student XLSX and returns a summary."""
    df = pd.read_excel(file_path)
    return df.to_string()
