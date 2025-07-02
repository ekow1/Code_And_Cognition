#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and debug URI issues
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongo_uri():
    """Test MongoDB URI parsing and connection"""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db = os.getenv("MONGO_DB", "fastapi_app")
    
    print(f"Testing MongoDB connection...")
    print(f"URI: {mongo_uri}")
    print(f"Database: {mongo_db}")
    
    # Clean the URI
    cleaned_uri = mongo_uri.strip()
    print(f"Cleaned URI: {cleaned_uri}")
    
    # Basic validation
    if not cleaned_uri.startswith(("mongodb://", "mongodb+srv://")):
        print("❌ Invalid MongoDB URI format")
        return False
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        async def test_connection():
            try:
                client = AsyncIOMotorClient(cleaned_uri)
                # Test the connection
                await client.admin.command("ping")
                print("✅ MongoDB connection successful!")
                return True
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                return False
        
        # Run the async test
        result = asyncio.run(test_connection())
        return result
        
    except ImportError:
        print("❌ Motor not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_mongo_uri()
    sys.exit(0 if success else 1) 