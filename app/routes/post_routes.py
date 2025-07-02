from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from app.model.post_model import PostCreate
from app.controllers import post_controller
from app.utils.auth_utils import get_token_from_cookie
import json

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

def safe_json_parse(field: str):
    """
    Parse a JSON string safely, or fallback to comma-separated values.
    """
    try:
        return json.loads(field)
    except json.JSONDecodeError:
        return [item.strip() for item in field.split(",") if item.strip()]

@router.post("/")
async def create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    categories: str = Form("[]"),
    tags: str = Form("[]"),
    image: UploadFile = File(None)
):
    user = get_token_from_cookie(request)

    # Use the safe parser here
    parsed_categories = safe_json_parse(categories)
    parsed_tags = safe_json_parse(tags)

    post = PostCreate(
        title=title,
        content=content,
        categories=parsed_categories,
        tags=parsed_tags
    )
    return await post_controller.create_post(post, user["user_id"], image)

@router.get("/me")
async def get_my_posts(request: Request):
    user = get_token_from_cookie(request)
    return await post_controller.get_user_posts(user["user_id"])

@router.put("/{post_id}/like")
async def like_post(post_id: str, request: Request):
    user = get_token_from_cookie(request)
    return await post_controller.like_post(post_id, user["user_id"])

@router.post("/{post_id}/comment")
async def comment_post(post_id: str, request: Request, text: str = Form(...)):
    user = get_token_from_cookie(request)
    return await post_controller.add_comment(post_id, user["user_id"], text)
