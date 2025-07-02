from fastapi import HTTPException, UploadFile
from app.db.mongo_db import db
from app.model.post_model import PostCreate
from bson import ObjectId
from datetime import datetime
from app.utils.supabase_utils import upload_image
def serialize_post(post):
    post["_id"] = str(post["_id"])
    post["author_id"] = str(post["author_id"])
    post["likes"] = [str(uid) for uid in post.get("likes", [])]
    for comment in post.get("comments", []):
        comment["user_id"] = str(comment["user_id"])
        comment["timestamp"] = comment["timestamp"].isoformat()
    return post

# Create a new post document
async def create_post(post: PostCreate, user_id: str, image_file: UploadFile = None):
    post_data = post.dict()
    if image_file:
        try:
            post_data["image"] = upload_image(image_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    post_data["author_id"] = ObjectId(user_id)
    post_data["created_at"] = datetime.utcnow()
    post_data["likes"] = []
    post_data["comments"] = []
    result = await db["posts"].insert_one(post_data)
    post_data["_id"] = str(result.inserted_id)
    post_data["author_id"] = user_id
    return post_data

# Retrieve all posts by a specific user
async def get_user_posts(user_id: str):
    posts = []
    async for post in db["posts"].find({"author_id": ObjectId(user_id)}):
        posts.append(serialize_post(post))
    return posts

# Like a post
async def like_post(post_id: str, user_id: str):
    result = await db["posts"].update_one(
        {"_id": ObjectId(post_id)},
        {"$addToSet": {"likes": ObjectId(user_id)}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Already liked or post not found")
    return {"message": "Post liked"}

# Add a comment
async def add_comment(post_id: str, user_id: str, text: str):
    comment = {
        "user_id": ObjectId(user_id),
        "text": text,
        "timestamp": datetime.utcnow()
    }
    result = await db["posts"].update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Comment added"}