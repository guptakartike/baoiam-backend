from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

# Define the expected JSON body structure
class LoginWelcomeRequest(BaseModel):
    name: str

# Changed from @router.get to @router.post
@router.post("/login-welcome")
def post_login_welcome_popup(payload: LoginWelcomeRequest):
    """
    Accepts a user's name and returns a personalized welcome popup message.
    """
    return {
        "message": f"Hi {payload.name}, welcome to our website! You have successfully logged in."
    }