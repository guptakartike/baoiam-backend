# main.py
from fastapi import FastAPI
from dotenv import load_dotenv

# 1. Load the .env file variables into system memory first!
load_dotenv()

# 2. Import your router after the env variables are ready
from app.routes.course_router import router as course_router

app = FastAPI(
    title=" EdTech Module — Local Test Environment",
    description="Running independently in VS Code before final code integration.",
    version="1.0"
)

# Connect your router to the application
app.include_router(course_router)

@app.get("/")
def root():
    return {"message":  "local course server is running! Go to /docs to test endpoints."}