# app/database.py
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "fastapi_app")

# Validate and clean MongoDB URI
def clean_mongo_uri(uri):
    """Clean and validate MongoDB URI"""
    if not uri:
        return "mongodb://localhost:27017"
    
    # Remove any trailing spaces or newlines
    uri = uri.strip()
    
    # Basic validation
    if not uri.startswith(("mongodb://", "mongodb+srv://")):
        logger.warning(f"Invalid MongoDB URI format: {uri}")
        return "mongodb://localhost:27017"
    
    return uri

try:
    cleaned_uri = clean_mongo_uri(MONGO_URI)
    logger.info(f"Connecting to MongoDB with URI: {cleaned_uri}")
    client = AsyncIOMotorClient(cleaned_uri)
    db = client[MONGO_DB]
    logger.info(f"Successfully connected to MongoDB database: {MONGO_DB}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    logger.error(f"URI was: {MONGO_URI}")
    raise
