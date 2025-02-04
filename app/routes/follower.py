from fastapi import APIRouter, HTTPException
from app.database import get_db

router = APIRouter()

@router.get("/{username}")
async def get_followers(username: str, page: int = 1, limit: int = 20):
    skip = (page - 1) * limit
    page_data = await db["pages"].find_one({"username": username})
    if not page_data:
        raise HTTPException(status_code=404, detail="Page not found")

    total = await db["followers"].count_documents({"page_id": page_data["id"]})
    followers = await db["followers"].find({"page_id": page["id"]}).skip(skip).limit(limit).to_list(length=limit)
    return {"total": total, "page": page, "limit": limit, "data": followers}
