from pydantic import BaseModel
from typing import Optional, List


class CourseCreate(BaseModel):
    """Schema for creating a new course (admin only)."""
    title: str
    description: str
    price: float


class CourseResponse(BaseModel):
    """Schema for returning course data."""
    id: int
    title: str
    description: str
    price: float
    instructor_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    """Schema for marking a lesson as completed."""
    lesson_id: int


class ProgressResponse(BaseModel):
    """Schema for returning course progress percentage."""
    course_id: int
    percent_complete: float


class ModuleResponse(BaseModel):
    """Schema for returning module data."""
    number: int
    title: str
    duration_hours: float

    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    """Schema for returning course in list/browse view."""
    id: int
    title: str
    category: Optional[str] = None
    price: float
    avg_salary: Optional[str] = None
    avg_time_to_hire: Optional[str] = None
    student_rating: Optional[float] = None
    tech_tags: Optional[str] = None

    class Config:
        from_attributes = True


class CourseDetailResponse(BaseModel):
    """Schema for returning full course detail view."""
    id: int
    title: str
    description: str
    category: Optional[str] = None
    price: float
    avg_salary: Optional[str] = None
    avg_time_to_hire: Optional[str] = None
    student_rating: Optional[float] = None
    tech_tags: Optional[str] = None
    modules: List[ModuleResponse] = []

    class Config:
        from_attributes = True