from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student

INITIAL_STUDENTS = [
    {"name": "Aditi Rao", "email": "aditi.rao@example.com", "age": 22},
    {"name": "Rohan Mehta", "email": "rohan.mehta@example.com", "age": 19},
    {"name": "Kavya Nair", "email": "kavya.nair@example.com", "age": 25},
    {"name": "Farhan Sheikh", "email": "farhan.sheikh@example.com", "age": 18},
    {"name": "Priya Iyer", "email": "priya.iyer@example.com", "age": 21},
    {"name": "Devansh Gupta", "email": "devansh.gupta@example.com", "age": 23},
    {"name": "Meera Joshi", "email": "meera.joshi@example.com", "age": 20},
    {"name": "Sameer Khan", "email": "sameer.khan@example.com", "age": 24},
]


def seed_data_if_empty(db: Session = None) -> bool:
    """
    Seed initial student records into the database ONLY if the Student table is currently empty.
    Returns True if seeding occurred, False otherwise.
    """
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        count = db.query(Student).count()
        if count == 0:
            for student_data in INITIAL_STUDENTS:
                db_student = Student(**student_data)
                db.add(db_student)
            db.commit()
            print("Successfully seeded 8 initial students into empty database.")
            return True
        else:
            print(f"Database already contains {count} students. Skipping seed.")
            return False
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_data_if_empty()
