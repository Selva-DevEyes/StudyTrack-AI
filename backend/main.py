import os
import sys
from typing import List, Optional

# Ensure backend directory is in python search path
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from contextlib import asynccontextmanager
from database import engine, Base, get_db
import crud
import schemas
import algorithms
import ai_service
from seed_data import seed_data_if_empty

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    # Seed data if empty
    seed_data_if_empty()
    yield

app = FastAPI(
    title="StudyTrack AI API",
    description="Intelligent Full-Stack Learning & Trainee Management Platform API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS explicitly (Never allow wildcard "*")
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# --- Student Routes ---

@app.post("/students/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a new student with email uniqueness check."""
    existing_student = crud.get_student_by_email(db, email=student.email)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student.email}' already exists."
        )
    return crud.create_student(db=db, student=student)


@app.get("/students/", response_model=List[schemas.StudentResponse])
def read_students(
    min_age: Optional[int] = Query(None, description="Filter students by minimum age"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all students, optionally filtered by minimum age."""
    students = crud.get_students(db=db, skip=skip, limit=limit, min_age=min_age)
    return students


@app.get("/students/sorted", response_model=List[schemas.StudentResponse])
def get_sorted_students(
    by: str = Query("age", description="Sort field: 'age' or 'name'"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all students sorted by specified field ('age' or 'name')
    using handwritten Insertion Sort algorithm.
    """
    if by not in ("age", "name"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'by' must be 'age' or 'name'."
        )
    students = crud.get_students(db=db, limit=1000)
    sorted_students = algorithms.insertion_sort_by_field(students, field=by)
    return sorted_students


@app.get("/students/search", response_model=schemas.StudentResponse)
def search_student_by_name(
    name: str = Query(..., description="Exact student name to search"),
    db: Session = Depends(get_db)
):
    """
    Search for a student by name using iterative Binary Search on a name-sorted array.
    """
    students = crud.get_students(db=db, limit=1000)
    sorted_students = sorted(students, key=lambda s: s.name)
    result = algorithms.binary_search_by_name(sorted_students, name=name)

    if result == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with name '{name}' not found."
        )
    return result


@app.get("/students/report")
def get_roster_report(
    min_age: int = Query(21, description="Minimum age filter threshold"),
    db: Session = Depends(get_db)
):
    """
    Generate a roster report and count of students meeting min_age criteria.
    """
    students = crud.get_students(db=db, limit=1000)
    count = algorithms.count_students_meeting_min_age(students, min_age=min_age)
    report_text = algorithms.format_roster_report(students)
    return {
        "report": report_text,
        "count_meeting_min_age": count
    }


@app.post("/students/reset-seed")
def reset_seed_data(db: Session = Depends(get_db)):
    """
    Reset and re-seed student roster with updated names from seed_data.py.
    """
    seed_data.seed_data_if_empty(db=db, force=True)
    return {"message": "Roster successfully re-seeded from seed_data.py"}


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Retrieve a single student by ID."""
    db_student = crud.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return db_student


@app.patch("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update student fields by ID."""
    # If updating email, check for duplicate
    if student_update.email is not None:
        existing = crud.get_student_by_email(db, email=student_update.email)
        if existing and existing.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{student_update.email}' is already in use by another student."
            )

    updated_student = crud.update_student(db, student_id=student_id, student_update=student_update)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return updated_student


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete student by ID."""
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return {"message": f"Student {student_id} deleted successfully."}


@app.get("/students/{student_id}/course-count")
def get_student_course_count(student_id: int, db: Session = Depends(get_db)):
    """Return total number of enrolled courses for student using database aggregate."""
    count = crud.get_student_course_count(db, student_id=student_id)
    if count is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return {"student_id": student_id, "course_count": count}


# --- Course Routes ---

@app.post("/courses/", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """Create a new course assigned to a student."""
    student = crud.get_student(db, student_id=course.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot create course: Student with ID {course.student_id} not found."
        )
    return crud.create_course(db=db, course=course)


@app.get("/courses/", response_model=List[schemas.CourseResponse])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all course records."""
    return crud.get_courses(db=db, skip=skip, limit=limit)


@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course by ID."""
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    return db_course


@app.patch("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    """Update course attributes by ID."""
    if course_update.student_id is not None:
        student = crud.get_student(db, student_id=course_update.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot update course: Student with ID {course_update.student_id} not found."
            )

    updated_course = crud.update_course(db, course_id=course_id, course_update=course_update)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    return updated_course


@app.delete("/courses/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete course by ID."""
    success = crud.delete_course(db, course_id=course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    return {"message": f"Course {course_id} deleted successfully."}


# --- AI Assistant Routes ---

@app.post("/assistant/summarize", response_model=schemas.SummarizeResponse)
def summarize_study_notes(payload: schemas.SummarizeRequest):
    """
    Summarize lecture/study notes using deterministic offline mock rules.
    """
    summary = ai_service.summarize_notes(payload.text)
    return summary


@app.get("/assistant/search")
def search_study_notes(query: str = Query("", description="Query string for semantic similarity search")):
    """
    Search and rank 5 pre-defined study notes using 12-dim mock embeddings and cosine similarity.
    """
    ranked_notes = ai_service.search_notes(query)
    return ranked_notes


# --- Static Files / Frontend Serving ---

backend_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.abspath(os.path.join(backend_dir, "..", "frontend"))

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static_files")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static_root")
