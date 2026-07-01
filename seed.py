from app.db.database import SessionLocal
from app.models.models import Course, Module

def seed():
    db = SessionLocal()

    try:
        # ── Course 1: Web Development ──
        course1 = Course(
            title="Full Stack Web Development",
            description="Learn HTML, CSS, JavaScript, and React to become a full stack web developer.",
            category="web-development",
            price=4999,
            avg_salary="6 LPA",
            avg_time_to_hire="3 months",
            student_rating=4.5,
            tech_tags="HTML, CSS, JavaScript, React",
        )
        db.add(course1)
        db.flush()

        db.add_all([
            Module(course_id=course1.id, number=1, title="HTML Basics", duration_hours=2),
            Module(course_id=course1.id, number=2, title="CSS Styling", duration_hours=3),
            Module(course_id=course1.id, number=3, title="JavaScript", duration_hours=5),
        ])

        # ── Course 2: Data Science ──
        course2 = Course(
            title="Data Science with Python",
            description="Master Python, Pandas, and Machine Learning to become a Data Scientist.",
            category="data-science",
            price=5999,
            avg_salary="8 LPA",
            avg_time_to_hire="2 months",
            student_rating=4.7,
            tech_tags="Python, Pandas, ML, SQL",
        )
        db.add(course2)
        db.flush()

        db.add_all([
            Module(course_id=course2.id, number=1, title="Python Basics", duration_hours=3),
            Module(course_id=course2.id, number=2, title="Pandas & Numpy", duration_hours=4),
            Module(course_id=course2.id, number=3, title="Machine Learning Intro", duration_hours=6),
        ])

        db.commit()
        print("✅ 2 courses with modules seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    seed()