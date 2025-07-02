import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException

# Load environment variables safely
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")

try:
    EXP_MINUTES = int(os.getenv("JWT_EXPIRES", "30").strip())
except ValueError:
    EXP_MINUTES = 30  # fallback if environment variable is invalid

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    """Verify a plain password against a hashed one."""
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    """Create a JWT token with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXP_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    """Decode a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_token_from_cookie(request: Request):
    """Extract and decode JWT token from cookies."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return decode_token(token)
