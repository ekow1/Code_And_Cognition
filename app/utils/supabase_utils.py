import os
from supabase import create_client
from uuid import uuid4

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image(file):
    filename = f"posts/{uuid4()}.jpg"
    content = file.file.read()
    response = supabase.storage.from_("post-images").upload(filename, content, {"content-type": "image/jpeg"})
    # ✅ Updated to check for `response.error` correctly instead of using `.get`
    if hasattr(response, "error") and response.error:
        raise Exception(f"Image upload failed: {response.error.message}")
    return f"{SUPABASE_URL}/storage/v1/object/public/post-images/{filename}"