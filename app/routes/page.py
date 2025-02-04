from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.scraper import scrape_facebook_page, save_to_mongo
from typing import Optional, List

router = APIRouter()

@router.get("/{username}")
async def get_page(username: str):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    page = await db["pages"].find_one({"username": username}) #await
    if page:
        return page
    
    scraped_data = await scrape_facebook_page(username)
    if scraped_data:
        await save_to_mongo(scraped_data)
        return scraped_data
    raise HTTPException(status_code=404, detail="Page not found")

@router.get("/")
async def search_pages(min_followers: int = 20000, max_followers: int = 40000, name: Optional[str] = None, page: int = 1, limit: int = 10):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    query = {"followers": {"$gte": min_followers, "$lte": max_followers}}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    skip = (page - 1) * limit
    total = await db["pages"].count_documents(query)
    pages = await db["pages"].find(query).skip(skip).limit(limit).to_list(length=limit)
    return {"total": len(pages), "page": page, "limit": limit,"data": pages}
