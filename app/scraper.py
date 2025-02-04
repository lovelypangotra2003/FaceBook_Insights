from playwright.async_api import async_playwright
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME is not set! Check your .env file.")
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

async def save_to_mongo(data):
    if not data:
        logger.error("No data to save!")
        return
    try:
        result = await db["pages"].update_one(
            {"username": data["username"]},
            {"$set": data},
            upsert=True
        )
        if result.upserted_id or result.modified_count > 0:
            logger.info(f"Data saved for {data['username']} in MongoDB!")
        else:
            logger.warning(f"No changes made to MongoDB for {data['username']}.")
    except Exception as e:
        logger.error(f"Failed to save data to MongoDB: {e}")

    
async def scrape_facebook_page(username: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = f"https://www.facebook.com/{username}"
        await page.goto(url, timeout=15000)
        try:
            # Extract Page Details
            page_name = await page.inner_text("h1") if await page.query_selector("h1") else None
            profile_pic = await page.get_attribute("img", "src") if await page.query_selector("img") else None

            # Extract Page ID from meta tags
            page_id_meta = await page.get_attribute("meta[property='al:android:url']", "content")
            page_id = page_id_meta.split("/")[-1] if page_id_meta else None

            # Extract Followers (Workaround as FB hides counts)
            followers_text = await page.inner_text("div[aria-label*='followers']") if await page.query_selector("div[aria-label*='followers']") else "0"
            followers = int(''.join(filter(str.isdigit, followers_text)))  # Convert to integer

            # Extract Category, Email, and Website
            category = await page.inner_text("div[role='contentinfo']") if await page.query_selector("div[role='contentinfo']") else None
            email = None
            website = None
            about_section = await page.inner_text("div[aria-label='About']") if await page.query_selector("div[aria-label='About']") else ""
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", about_section)
            website_match = re.search(r"https?://[^\s]+", about_section)

            if email_match:
                email = email_match.group(0)
            if website_match:
                website = website_match.group(0)

            # Extract Follower & Like Count
            followers = 0
            likes = 0
            stats_section = await page.inner_text("div[aria-label='Community']") if await page.query_selector("div[aria-label='Community']") else ""
            followers_match = re.search(r"([\d,]+)\s*Followers", stats_section)
            likes_match = re.search(r"([\d,]+)\s*Likes", stats_section)

            if followers_match:
                followers = int(followers_match.group(1).replace(",", ""))
            if likes_match:
                likes = int(likes_match.group(1).replace(",", ""))

            # Extract Page Creation Date
            creation_date = None
            creation_date_match = re.search(r"Page created on (.+)", about_section)
            if creation_date_match:
                creation_date = creation_date_match.group(1)
            
            # Extract Recent Posts (25-40)
            posts = []
            post_elements = await page.query_selector_all("div[data-ad-comet-preview]")
            for post in post_elements[:40]:  # Limit to 40 posts
                content = await post.inner_text() if post else None
                likes = 0
                comments = []
                
                # Extract Likes Count for Post
                likes_element = await post.query_selector("span[aria-label*='like']")
                if likes_element:
                    likes_text = await likes_element.inner_text()
                    likes = int(re.sub(r'\D', '', likes_text)) if re.search(r'\d+', likes_text) else 0

                # Extract Comments on Post
                comment_elements = await post.query_selector_all("div[aria-label='Comment']")
                for comment in comment_elements:
                    comment_text = await comment.inner_text()
                    comments.append({"text": comment_text})

                posts.append({
                    "content": content,
                    "likes": likes,
                    "comments": comments
                })

            # # Extract Followers (if available)
            # followers_list = []
            # follower_elements = await page.query_selector_all("div[aria-label='Followers']")
            # for follower in follower_elements:
            #     name = await follower.inner_text()
            #     profile_pic = await follower.get_attribute("img", "src") if await follower.query_selector("img") else None
            #     followers_list.append({"name": name, "profile_pic": profile_pic})

            # # Extract Following (if available)
            # following_list = []
            # following_elements = await page.query_selector_all("div[aria-label='Following']")
            # for following in following_elements:
            #     name = await following.inner_text()
            #     profile_pic = await following.get_attribute("img", "src") if await following.query_selector("img") else None
            #     following_list.append({"name": name, "profile_pic": profile_pic})


            await browser.close()
            return {
                "username": username,
                "page_id": page_id,
                "name": page_name,
                "profile_pic": profile_pic,
                "url": url,
                "followers": followers,
                "category": category,
                "email": email,
                "website": website,
                "followers": followers,
                "likes": likes,
                "creation_date": creation_date,
                "posts": posts,
                # "followers_list": followers_list,
                # "following_list": following_list
            }

        except Exception as e:
            await browser.close()
            logger.error(f"Scraping failed for {username}: {e}")
            return None

# Testing scraper
if __name__ == "__main__":
    result = asyncio.run(scrape_facebook_page("boat.lifestyle"))
    print(result)
