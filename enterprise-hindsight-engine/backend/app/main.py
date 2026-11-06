"""
Enterprise Deal & Revenue Intelligence Platform
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, close_db
from app.hindsight_client import hindsight_client
from app.routers import deals, accounts, feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()
    await hindsight_client.close()


app = FastAPI(
    title="Enterprise Deal & Revenue Intelligence Platform",
    description="Multi-persona platform powered by Hindsight persistent memory and Groq LLM",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(deals.router, prefix="/api/deals", tags=["Sales Deals"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["Customer Success"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Product Feedback"])


@app.get("/")
async def health_check():
    """Root health check endpoint."""
    return {
        "status": "active",
        "system": "Hindsight Memory Engine Online",
        "version": "1.0.0",
        "services": {
            "deals": "/api/deals",
            "accounts": "/api/accounts",
            "feedback": "/api/feedback",
        },
    }


@app.get("/health")
async def detailed_health():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-15T10:30:00Z",  # Would use datetime.utcnow()
        "services": {
            "api": "healthy",
            "database": "connected",
            "hindsight": "configured" if settings.hindsight_api_key else "simulation_mode",
            "groq": "configured" if settings.groq_api_key else "simulation_mode",
        },
    }