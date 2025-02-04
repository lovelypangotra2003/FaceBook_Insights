from motor.motor_asyncio import AsyncIOMotorClient
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')

try:
    client = AsyncIOMotorClient(MONGO_URI) 
    db = client[DATABASE_NAME]
    logger.info(f"Connected to MongoDB successfully: {DATABASE_NAME}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    db = None

def get_db():
    return db
