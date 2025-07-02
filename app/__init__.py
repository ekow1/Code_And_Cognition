# app/__init__.py
import logging
from fastapi import FastAPI
from app.db.mongo_db import client
from app.routes.auth_routes import router as auth_router
from app.routes.post_routes import router as post_routes
from app.routes.health_routes import router as health_router

# ✅ Proper logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI MongoDB App",
    description="A FastAPI application with MongoDB integration",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(post_routes, prefix="/api/posts", tags=["Posts"])
app.include_router(health_router, tags=["Health"])

@app.on_event("startup")
async def startup_db_client():
    try:
        await client.admin.command("ping")
        logger.info("✅ MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("🛑 MongoDB connection closed.")
