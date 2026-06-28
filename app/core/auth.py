import os
import random
import requests
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.db.database import get_db
from app.models.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/verify-otp")


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def send_otp_msg91(phone: str, otp: str) -> bool:
    url = "https://api.msg91.com/api/v5/otp"
    payload = {
        "mobile": f"91{phone}",
        "otp": otp,
        "template_id": os.getenv("MSG91_TEMPLATE_ID"),
        "authkey": os.getenv("MSG91_API_KEY"),
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200


def is_otp_valid(otp_record) -> bool:
    if otp_record.is_used:
        return False
    if otp_record.expires_at < datetime.utcnow():
        return False
    return True


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user