from pydantic import BaseModel
from typing import List, Optional

class PostCreate(BaseModel):
    title: str
    content: str
    image: Optional[str] = None
    categories: Optional[List[str]] = []
    tags: Optional[List[str]] = []