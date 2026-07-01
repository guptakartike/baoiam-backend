from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


# ──────────────────────────────────────────────
# USER TABLE
# ──────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")
    taught_courses = relationship("Course", back_populates="instructor")


# ──────────────────────────────────────────────
# COURSE TABLE
# ──────────────────────────────────────────────
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    instructor = relationship("User", back_populates="taught_courses")
    enrollments = relationship("Enrollment", back_populates="course")
    payments = relationship("Payment", back_populates="course")
    modules = relationship("Module", back_populates="course")

# ──────────────────────────────────────────────
# ENROLLMENT TABLE
# ──────────────────────────────────────────────
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    status = Column(String, default="active")
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


# ──────────────────────────────────────────────
# PAYMENT TABLE
# ──────────────────────────────────────────────
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    razorpay_order_id = Column(String, nullable=False)
    razorpay_payment_id = Column(String)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")
    course = relationship("Course", back_populates="payments")


# ──────────────────────────────────────────────
# PROGRESS TABLE
# ──────────────────────────────────────────────
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer)
    completed = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_records")


# ──────────────────────────────────────────────
# MODULE TABLE
# ──────────────────────────────────────────────
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    duration_hours = Column(Float, nullable=False)

    # Relationship
    course = relationship("Course", back_populates="modules")