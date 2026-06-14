import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter(tags=["Courses & Progress"])

# =====================================================================
# DYNAMIC ENVIRONMENT CONFIGURATION
# Reads the configuration value directly from your secure .env file!
# =====================================================================
# Fetch the setting as a string, and compare it to handle the boolean switch
INTEGRATION_MODE_STR = os.getenv("INTEGRATION_MODE", "False")
INTEGRATION_MODE = INTEGRATION_MODE_STR.strip().lower() in ("true", "1")

# =====================================================================
# 1. PYDANTIC SCHEMAS (All 3 required schemas are now accounted for!)
# =====================================================================
class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float

class ProgressUpdate(BaseModel):
    lesson_id: int

class ProgressResponse(BaseModel):
    course_id: int
    percent_complete: float

# =====================================================================
# MOCK DATA FOR LOCAL TESTING (Day 1)
# =====================================================================
MOCK_COURSES = [
    {"id": 1, "title": "FastAPI Masterclass", "description": "Learn to build production backend APIs.", "price": 499.0},
    {"id": 2, "title": "Java Mastery", "description": "Deep dive into OOP concepts and multi-threading.", "price": 799.0}
]

# Simulated progress database: user has completed 3 out of 5 lessons for course 1
MOCK_PROGRESS = {
    "course_id": 1,
    "completed_lessons": 3,
    "total_lessons": 5
}

# =====================================================================
# 2. ENDPOINTS IMPLEMENTATION
# =====================================================================

# Route 1: List all courses (Public)
@router.get("/courses", response_model=List[CourseResponse])
def get_all_courses():
    return MOCK_COURSES

# Route 2: Get Single Course Details (Public)
@router.get("/courses/{id}", response_model=CourseResponse)
def get_course_by_id(id: int):
    # Search for the course by its ID
    for course in MOCK_COURSES:
        if course["id"] == id:
            return course
    # Raise a clear error if the ID doesn't exist
    raise HTTPException(status_code=404, detail="Course not found")

# Route 3: Get User's Enrolled Courses (Protected)
@router.get("/my-courses", response_model=List[CourseResponse])
def get_my_courses():
    # Simulating returning only the course the user is enrolled in (Java Mastery)
    return [MOCK_COURSES[1]]

# Route 4: Update Lesson Progress (Protected)
@router.post("/progress/update")
def update_progress(payload: ProgressUpdate):
    return {
        "status": "mock_success",
        "message": f"Local test: Lesson {payload.lesson_id} successfully completed."
    }

# Route 5: Get Course Completion Percentage (Protected)
@router.get("/progress/{course_id}", response_model=ProgressResponse)
def get_course_progress(course_id: int):
    if course_id == MOCK_PROGRESS["course_id"]:
        # Applying the explicit assignment formula: (completed / total) * 100
        percentage = (MOCK_PROGRESS["completed_lessons"] / MOCK_PROGRESS["total_lessons"]) * 100
        return {
            "course_id": course_id,
            "percent_complete": percentage
        }
    
    # Default return fallback if they check progress on another course ID locally
    return {
        "course_id": course_id,
        "percent_complete": 0.0
    }