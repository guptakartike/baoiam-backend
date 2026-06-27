from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import Course, Enrollment, Progress
from app.core.auth import get_current_user, get_current_admin
from app.schemas.course import CourseCreate, CourseResponse, ProgressUpdate, ProgressResponse, CourseListResponse, CourseDetailResponse
router = APIRouter(tags=["Courses & Progress"])


# ──────────────────────────────────────────────
# 1. LIST ALL COURSES (Public)
# ──────────────────────────────────────────────
@router.get("/courses", response_model=List[CourseResponse])
def get_all_courses(category: str = None, db: Session = Depends(get_db)):
    """Return all available courses, optionally filtered by category."""
    query = db.query(Course)
    if category:
        query = query.filter(Course.category == category)
    courses = query.all()
    return courses


# ──────────────────────────────────────────────
# 2. GET SINGLE COURSE (Public)
# ──────────────────────────────────────────────
@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    """Return a single course by its ID."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ──────────────────────────────────────────────
# 3. CREATE A COURSE (Admin only)
# ──────────────────────────────────────────────
@router.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """Create a new course (admin only)."""
    new_course = Course(
        title=payload.title,
        description=payload.description,
        price=payload.price,
        instructor_id=current_user.id,
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


# ──────────────────────────────────────────────
# 4. GET ENROLLED COURSES (Protected)
# ──────────────────────────────────────────────
@router.get("/my-courses", response_model=List[CourseResponse])
def get_my_courses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Return all courses the authenticated user is enrolled in."""
    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id, Enrollment.status == "active")
        .all()
    )
    course_ids = [e.course_id for e in enrollments]
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
    return courses


# ──────────────────────────────────────────────
# 5. UPDATE LESSON PROGRESS (Protected)
# ──────────────────────────────────────────────
@router.post("/progress/update")
def update_progress(
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Mark a lesson as completed for the authenticated user."""
    # Check if progress record already exists
    existing = (
        db.query(Progress)
        .filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id == payload.lesson_id,
        )
        .first()
    )

    if existing:
        existing.completed = True
        db.commit()
        return {"status": "updated", "message": f"Lesson {payload.lesson_id} marked as completed."}

    new_progress = Progress(
        user_id=current_user.id,
        lesson_id=payload.lesson_id,
        completed=True,
    )
    db.add(new_progress)
    db.commit()
    return {"status": "created", "message": f"Lesson {payload.lesson_id} marked as completed."}


# ──────────────────────────────────────────────
# 6. GET COURSE PROGRESS (Protected)
# ──────────────────────────────────────────────
@router.get("/progress/{course_id}", response_model=ProgressResponse)
def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Return the user's completion percentage for a specific course."""
    # Count total lessons and completed lessons for this user in this course
    total_lessons = db.query(Progress).filter(
        Progress.user_id == current_user.id,
    ).count()

    completed_lessons = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.completed == True,
    ).count()

    if total_lessons == 0:
        percent = 0.0
    else:
        percent = (completed_lessons / total_lessons) * 100

    return {
        "course_id": course_id,
        "percent_complete": percent,
    }
