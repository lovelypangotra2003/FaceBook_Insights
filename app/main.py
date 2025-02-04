from fastapi import FastAPI
from app.routes import page, post, follower
# from app.database import connect_db

app = FastAPI(title="Facebook Insights Microservice")
# Include routes
app.include_router(page.router, prefix="/pages", tags=["pages"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(follower.router, prefix="/followers", tags=["followers"])
# Root endpoint
@app.get("/")
async def root():
    return {"message": "Facebook Insights Microservice is running!"}
