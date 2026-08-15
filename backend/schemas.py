from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CourseBase(BaseModel):
    course_name: str = Field(..., min_length=1, description="Course name is required")
    credits: int = Field(..., ge=1, le=6, description="Credits must be between 1 and 6")


class CourseCreate(CourseBase):
    student_id: int = Field(..., gt=0, description="Valid student ID required")


class CourseUpdate(BaseModel):
    course_name: Optional[str] = Field(None, min_length=1)
    credits: Optional[int] = Field(None, ge=1, le=6)
    student_id: Optional[int] = Field(None, gt=0)


class CourseResponse(CourseBase):
    id: int
    student_id: int

    model_config = ConfigDict(from_attributes=True)


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, description="Student name is required")
    email: str = Field(..., min_length=1, description="Email is required")
    age: int = Field(..., gt=0, description="Age must be a positive integer")

    @field_validator("email")
    @classmethod
    def validate_email_contains_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email must contain '@'")
        return value.strip()


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)

    @field_validator("email")
    @classmethod
    def validate_email_contains_at(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if "@" not in value:
                raise ValueError("Email must contain '@'")
            return value.strip()
        return value


class StudentResponse(StudentBase):
    id: int
    courses: List[CourseResponse] = []

    model_config = ConfigDict(from_attributes=True)


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text of lecture or study notes to summarize")


class SummarizeResponse(BaseModel):
    topic: str
    key_points: List[str]
    difficulty: str

