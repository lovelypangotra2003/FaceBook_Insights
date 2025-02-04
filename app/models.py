from pydantic import BaseModel, ConfigDict
from typing import List,Optional
import datetime

class Page(BaseModel):
    id: str
    name: str
    username: str
    url: str
    profile_pic: Optional[str]
    email: Optional[str]
    website: Optional[str]
    category: Optional[str]
    followers: int = 0
    likes: int = 0
    creation_date: Optional[str]
    # last_scraped: Optional[str]


class Comment(BaseModel):
    user_id: str
    username: str
    profile_pic: Optional[str]
    text: str
    timestamp: datetime

class Post(BaseModel):
    id: str  # Facebook Post ID
    page_id: str
    content: Optional[str]
    likes: int
    comments: List[dict] = []
    created_at: str

class Follower(BaseModel):
    page_id: str  # The Page this user follows
    follower_id: str
    username: str
    profile_pic: Optional[str]
