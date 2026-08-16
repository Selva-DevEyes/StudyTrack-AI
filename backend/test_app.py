"""
Comprehensive End-to-End Test Suite for StudyTrack AI.
Tests every API endpoint, model validation, error case, algorithm, and AI feature.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import app
from database import engine, Base, get_db
import crud
import schemas
import algorithms
import ai_service


@pytest.fixture(autouse=True)
def setup_database():
    """Reset database tables before each test run."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as c:
        yield c


def test_seed_data_on_startup(client):
    """Verify that empty database is automatically seeded with 8 exact students."""
    response = client.get("/students/")
    assert response.status_code == 200
    students = response.json()
    assert len(students) == 8
    names = [s["name"] for s in students]
    assert "Selvam" in names
    assert "Sameer Khan" in names


def test_student_validation(client):
    """Test custom email validation (@ check) and age validation (gt=0)."""
    # Missing @ in email
    r1 = client.post("/students/", json={"name": "No At", "email": "invalidemail.com", "age": 20})
    assert r1.status_code == 422

    # Negative age
    r2 = client.post("/students/", json={"name": "Neg Age", "email": "neg@example.com", "age": -1})
    assert r2.status_code == 422

    # Age 0
    r3 = client.post("/students/", json={"name": "Zero Age", "email": "zero@example.com", "age": 0})
    assert r3.status_code == 422


def test_student_duplicate_email(client):
    """Test duplicate email rejection with 400 Bad Request."""
    r1 = client.post("/students/", json={"name": "Original", "email": "unique@example.com", "age": 21})
    assert r1.status_code == 201

    r2 = client.post("/students/", json={"name": "Duplicate", "email": "unique@example.com", "age": 22})
    assert r2.status_code == 400
    assert "already exists" in r2.json()["detail"]


def test_student_crud(client):
    """Test full CRUD operations on Student."""
    # Create
    r = client.post("/students/", json={"name": "John Doe", "email": "john.doe@example.com", "age": 24})
    assert r.status_code == 201
    s_id = r.json()["id"]

    # Read Single
    r_get = client.get(f"/students/{s_id}")
    assert r_get.status_code == 200
    assert r_get.json()["name"] == "John Doe"

    # Patch
    r_patch = client.patch(f"/students/{s_id}", json={"age": 25})
    assert r_patch.status_code == 200
    assert r_patch.json()["age"] == 25

    # Delete
    r_del = client.delete(f"/students/{s_id}")
    assert r_del.status_code == 200

    # 404 after delete
    r_404 = client.get(f"/students/{s_id}")
    assert r_404.status_code == 404


def test_course_crud_and_aggregate_count(client):
    """Test Course creation, credits constraint, and SQL aggregate course-count."""
    # Get a seeded student
    s_res = client.get("/students/")
    student_id = s_res.json()[0]["id"]

    # Initial course count should be 0
    cnt_res = client.get(f"/students/{student_id}/course-count")
    assert cnt_res.status_code == 200
    assert cnt_res.json()["course_count"] == 0

    # Add valid course (credits 1 to 6)
    c_res = client.post("/courses/", json={"course_name": "Algorithms", "credits": 4, "student_id": student_id})
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

    # Course count should now be 1
    cnt_res2 = client.get(f"/students/{student_id}/course-count")
    assert cnt_res2.json()["course_count"] == 1

    # Invalid credits (>6)
    c_invalid = client.post("/courses/", json={"course_name": "Over Credited", "credits": 10, "student_id": student_id})
    assert c_invalid.status_code == 422

    # Delete course
    del_res = client.delete(f"/courses/{c_id}")
    assert del_res.status_code == 200


def test_insertion_sort_inplace_and_endpoints(client):
    """Test in-place insertion_sort_by_field and GET /students/sorted?by=age."""
    # Test in-place mutation
    sample = [{'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 20}]
    res = algorithms.insertion_sort_by_field(sample, 'age')
    assert res is sample
    assert sample[0]['name'] == 'Alice'

    r_age = client.get("/students/sorted?by=age")
    assert r_age.status_code == 200
    ages = [s["age"] for s in r_age.json()]
    assert ages == sorted(ages)

    r_name = client.get("/students/sorted?by=name")
    assert r_name.status_code == 200
    names = [s["name"] for s in r_name.json()]
    assert names == sorted(names)


def test_binary_search_endpoint(client):
    """Test GET /students/search?name=... with found and 404 cases."""
    r_found = client.get("/students/search?name=Selvam")
    assert r_found.status_code == 200
    assert r_found.json()["name"] == "Selvam"

    r_notfound = client.get("/students/search?name=Ghost User")
    assert r_notfound.status_code == 404


def test_report_endpoint(client):
    """Test GET /students/report?min_age=... format '[Age {age}] {name} <{email}>'"""
    r = client.get("/students/report?min_age=21")
    assert r.status_code == 200
    res = r.json()
    assert "report" in res
    assert res["count_meeting_min_age"] == 6
    assert "[Age 32] Selvam <selvam@example.com>" in res["report"]


def test_ai_summarizer_endpoint(client):
    """Test POST /assistant/summarize with normal and empty input."""
    r1 = client.post("/assistant/summarize", json={"text": "Pydantic Models\nPydantic handles data validation. It generates schemas. FastAPI integrates it."})
    assert r1.status_code == 200
    res1 = r1.json()
    assert res1["topic"] == "Pydantic Models"
    assert len(res1["key_points"]) == 3
    assert res1["difficulty"] == "easy"

    r2 = client.post("/assistant/summarize", json={"text": "   "})
    assert r2.status_code == 200
    res2 = r2.json()
    assert res2 == {"topic": "untitled", "key_points": [], "difficulty": "easy"}


def test_ai_semantic_search_endpoint(client):
    """Test GET /assistant/search?query=... checking id field and ranking."""
    r1 = client.get("/assistant/search?query=fastapi pydantic validate")
    assert r1.status_code == 200
    res1 = r1.json()
    assert len(res1) == 5
    assert res1[0]["id"] == 3 # Note 3 is about FastAPI and Pydantic

    r2 = client.get("/assistant/search?query=unmatched terms 12345")
    assert r2.status_code == 200
    res2 = r2.json()
    assert len(res2) == 5
    for note in res2:
        assert note["score"] == 0.0
    assert [n["id"] for n in res2] == [1, 2, 3, 4, 5]
