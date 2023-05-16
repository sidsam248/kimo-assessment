import sys
import os
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Get the root directory path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root directory path to the system path
sys.path.append(root_path)

from app import app

client = TestClient(app)

# Test for index function
def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# Tests for 'get_courses' end point
def test_get_courses_alphabetical():
    response = client.get("/courses?sort_by=alphabetical")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    names = [course["name"] for course in data]
    assert names == sorted(names)

def test_get_courses_date():
    response = client.get("/courses?sort_by=date")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    dates = [course["date"] for course in data]  
    assert dates == sorted(dates, reverse=True)

def test_get_courses_rating():
    response = client.get("/courses?sort_by=rating")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    ratings = [course["ratings"] for course in data]  
    assert ratings == sorted(ratings, reverse=True)

# Tests for 'get_course' end point
def test_get_course():
    course_id = "6462ef473371831c4916e459"

    response = client.get(f"/course/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    course = data[0]
    assert course["_id"] == course_id

def test_get_course_not_found():
    course_id = "non-existent-id"

    response = client.get(f"/course/{course_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Course {course_id} not found"

# Tests for 'get_chapter' end point
def test_get_chapter_by_name_found():
    chapter_name = "Image Classification"

    response = client.get(f"/chapters/{chapter_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == chapter_name


def test_get_chapter_by_name_not_found():
    chapter_name = "Non-existent Chapter"

    response = client.get(f"/chapters/{chapter_name}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Chapter {chapter_name} not found"

# Tests for 'rate_chapter' end point
def test_rate_chapter_positive_rating():
    course_id = "6462ef473371831c4916e459"
    chapter_name = "Image Classification"
    rating = "Positive"

    body = {"course_id": course_id, "chapter_name": chapter_name, "rating": rating}

    response = client.post(f"/rate_chapter?course_id={course_id}&chapter_name={chapter_name}&rating={rating}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Rating submitted successfully"


def test_rate_chapter_negative_rating():
    course_id = "6462ef473371831c4916e459"
    chapter_name = "Image Classification"
    rating = "Negative"

    response = client.post(f"/rate_chapter?course_id={course_id}&chapter_name={chapter_name}&rating={rating}")
    data = response.json()
    assert data["message"] == "Rating submitted successfully"


def test_rate_chapter_not_found():
    course_id = "6462ef473371831c4916e459"
    chapter_name = "Non-existent Chapter"
    rating = "Positive"

    response = client.post(f"/rate_chapter?course_id={course_id}&chapter_name={chapter_name}&rating={rating}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Chapter {chapter_name} not found"


def test_rate_chapter_invalid_course_id():
    course_id = "invalid-course-id"
    chapter_name = "Image Classification"
    rating = "Positive"

    response = client.post(f"/rate_chapter?course_id={course_id}&chapter_name={chapter_name}&rating={rating}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Course {course_id} not found"