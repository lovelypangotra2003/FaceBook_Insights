import asyncio
from database import db
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_insertion():
    scraped_data = {
        "username": "boat.lifestyle",
        "page_id": "100064894590088",
        "name": "boAt",
        "profile_pic": "https://example.com/image.jpg",
        "url": "https://www.facebook.com/boat.lifestyle",
        "followers": 5000,
        "category": "Electronics",
        "email": "contact@boat.com",
        "website": "https://www.boat-lifestyle.com",
        "likes": 10000,
        "creation_date": "2020-01-01",
        "posts": [{"content": "New product launch!", "likes": 200, "comments": []}]
    }

    try:
        result = await db["pages"].insert_one(scraped_data)  # ✅ Correct async usage
        logger.info(f"Data inserted! ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")

# Run the test
asyncio.run(test_insertion())
