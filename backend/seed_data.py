from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student

INITIAL_STUDENTS = [
    {"name": "Selvam", "email": "selvam@example.com", "age": 32},
    {"name": "Kanaga Selvi", "email": "kanagaselvi@example.com", "age": 30},
    {"name": "Muthamil", "email": "muthamil@example.com", "age": 25},
    {"name": "Vetri", "email": "vetri@example.com", "age": 18},
    {"name": "Robinson", "email": "robinson@example.com", "age": 21},
    {"name": "Irfan", "email": "irfan@example.com", "age": 23},
    {"name": "Vicky", "email": "vicky@example.com", "age": 20},
    {"name": "Sameer Khan", "email": "sameer.khan@example.com", "age": 24},
]


def seed_data_if_empty(db: Session = None, force: bool = False) -> bool:
    """
    Seed initial student records into the database.
    If force=True, clears existing students and reseeds with INITIAL_STUDENTS.
    If force=False, seeds only if Student table is empty.
    """
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        count = db.query(Student).count()
        if count == 0 or force:
            if force:
                db.query(Student).delete()
                db.commit()
            for student_data in INITIAL_STUDENTS:
                db_student = Student(**student_data)
                db.add(db_student)
            db.commit()
            print(f"Successfully seeded {len(INITIAL_STUDENTS)} initial students into database.")
            return True
        else:
            print(f"Database already contains {count} students. Skipping seed.")
            return False
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_data_if_empty(force=True)
