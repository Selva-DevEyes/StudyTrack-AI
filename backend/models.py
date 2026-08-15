from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)

    # Bidirectional relationship with Course
    courses = relationship("Course", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}', age={self.age})>"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    # Check constraint for credits (1 through 6)
    __table_args__ = (
        CheckConstraint("credits >= 1 AND credits <= 6", name="check_credits_range"),
    )

    # Bidirectional relationship with Student
    student = relationship("Student", back_populates="courses")

    def __repr__(self):
        return f"<Course(id={self.id}, course_name='{self.course_name}', credits={self.credits}, student_id={self.student_id})>"
