from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user_router import router as user_router
from app.routes.payment_router import router as payment_router
from app.routes.course_router import router as course_router
from app.routes.stats_router import router as stats_router

app = FastAPI(
    title="Baoiam EdTech Platform",
    description="Backend API for the Baoiam ed-tech platform — authentication, courses, payments, and progress tracking.",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user_router)
app.include_router(payment_router)
app.include_router(course_router)
app.include_router(stats_router)


@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint."""
    return {"status": "ok"}
