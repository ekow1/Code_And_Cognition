from fastapi import APIRouter, Response, Request, Depends
from app.model.user_model import UserRegister, UserLogin, UserUpdate
from app.controllers import auth_controller

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# ✅ Register new user
@router.post("/register")
async def register(user: UserRegister):
    return await auth_controller.register_user(user)


# ✅ Login user and set JWT token in cookie
@router.post("/login")
async def login(credentials: UserLogin, response: Response):
    return await auth_controller.login_user(credentials, response)


# ✅ Logout user by clearing cookie
@router.post("/logout")
async def logout(response: Response):
    return await auth_controller.logout_user(response)


# ✅ Get all users
@router.get("/users")
async def get_users():
    return await auth_controller.get_all_users()
