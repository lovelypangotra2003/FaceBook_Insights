from fastapi import APIRouter, HTTPException
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/{username}")
async def get_recent_posts(username: str, limit: int = 10):
    page = await db["pages"].find_one({"username": username})
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    total = await db["posts"].count_documents({"page_id": page["id"]})
    posts = await db["posts"].find({"page_id": page["id"]}).sort("created_at", -1).limit(limit).to_list(length=limit)
    return {"total": total, "limit": limit, "data": posts}
