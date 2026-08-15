from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student, Course
from schemas import StudentCreate, StudentUpdate, CourseCreate, CourseUpdate


# --- Student CRUD Operations ---

def get_student(db: Session, student_id: int) -> Optional[Student]:
    """Retrieve a single student by primary key ID."""
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """Retrieve a student by unique email address."""
    return db.query(Student).filter(Student.email == email).first()


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_age: Optional[int] = None
) -> List[Student]:
    """Retrieve all students with optional pagination and min_age filtering."""
    query = db.query(Student)
    if min_age is not None:
        query = query.filter(Student.age >= min_age)
    return query.offset(skip).limit(limit).all()


def create_student(db: Session, student: StudentCreate) -> Student:
    """Create a new student record."""
    db_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(
    db: Session,
    student_id: int,
    student_update: StudentUpdate
) -> Optional[Student]:
    """Update an existing student record."""
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> bool:
    """Delete a student record by ID."""
    db_student = get_student(db, student_id)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True


def get_student_course_count(db: Session, student_id: int) -> Optional[int]:
    """
    Return the total course count for a student using a database SQL aggregate
    (func.count) rather than Python len(). Returns None if student does not exist.
    """
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    count = db.query(func.count(Course.id))\
              .filter(Course.student_id == student_id)\
              .scalar()
    return count or 0


# --- Course CRUD Operations ---

def get_course(db: Session, course_id: int) -> Optional[Course]:
    """Retrieve a single course by primary key ID."""
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    """Retrieve all course records."""
    return db.query(Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: CourseCreate) -> Course:
    """Create a new course record."""
    db_course = Course(
        course_name=course.course_name,
        credits=course.credits,
        student_id=course.student_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(
    db: Session,
    course_id: int,
    course_update: CourseUpdate
) -> Optional[Course]:
    """Update an existing course record."""
    db_course = get_course(db, course_id)
    if not db_course:
        return None

    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)

    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int) -> bool:
    """Delete a course record by ID."""
    db_course = get_course(db, course_id)
    if not db_course:
        return False
    db.delete(db_course)
    db.commit()
    return True
