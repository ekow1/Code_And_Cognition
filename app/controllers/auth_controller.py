from fastapi import HTTPException, Response, Request, Depends
from app.db.mongo_db import db
from app.model.user_model import UserRegister, UserLogin, UserUpdate
from app.utils.auth_utils import hash_password, verify_password, create_token, decode_token
from bson import ObjectId
from datetime import datetime

# Registers new users
async def register_user(user: UserRegister):
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["created_at"] = datetime.utcnow()
    await db["users"].insert_one(user_dict)
    return {"message": "User registered successfully"}


# ---------------- Login ----------------
async def login_user(credentials: UserLogin, response: Response):
    user = await db["users"].find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"user_id": str(user["_id"]), "email": user["email"]})
    
    # Set token in HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # set to True in production with HTTPS
        samesite="lax"
    )
    
    return {"message": "Login successful"}

# ---------------- Get All Users ----------------
async def get_all_users():
    users = []
    cursor = db["users"].find()
    async for user in cursor:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        users.append(user)
    return users

# ---------------- Get User Profile ----------------
async def get_user_profile(user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    user.pop("password", None)
    return user

# ---------------- Update Profile ----------------
async def update_user_profile(user_id: str, user: UserUpdate):
    existing_user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email != existing_user["email"]:
        email_check = await db["users"].find_one({"email": user.email})
        if email_check:
            raise HTTPException(status_code=400, detail="Email already in use")

    update_data = user.dict()
    if user.password:
        update_data["password"] = hash_password(user.password)

    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return {"message": "User profile updated successfully"}

# ---------------- Delete User ----------------
async def delete_user(user_id: str):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# ---------------- Change Password ----------------
async def change_password(user_id: str, new_password: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed = hash_password(new_password)
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"password": hashed}})
    return {"message": "Password changed successfully"}

# ---------------- Logout ----------------
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
