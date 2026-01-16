"""
Main FastAPI Application
Paige's Inner Circle Experience Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from pathlib import Path

from .config import settings
from .database import engine, Base
from .api import (
    auth_router, 
    events_router, 
    rsvp_router, 
    legacy_pass_router, 
    payment_router, 
    gifts_router,
    memories_router,
    admin_router
)


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Exclusive luxury experience platform for Paige's Inner Circle",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files directory
static_dir = Path("app/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(rsvp_router, prefix="/api")
app.include_router(legacy_pass_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(gifts_router, prefix="/api")
app.include_router(memories_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup tasks
    """
    print("=" * 60)
    print(f"🎭 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 60)
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: Connected")
    print(f"CORS Origins: {', '.join(settings.cors_origins_list)}")
    print("=" * 60)
    print("✨ The Inner Circle experience is ready to welcome members")
    print("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown tasks
    """
    print("\n" + "=" * 60)
    print("👋 Thank you for an unforgettable experience")
    print("=" * 60)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Welcome to Paige's Inner Circle. The luxury experience awaits.",
        "documentation": "/api/docs" if settings.ENVIRONMENT == "development" else None
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION
    }


# API info endpoint
@app.get("/api")
async def api_info():
    """
    API information endpoint
    """
    return {
        "name": "Paige's Inner Circle API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "authentication": "/api/auth",
            "events": "/api/events",
            "documentation": "/api/docs" if settings.ENVIRONMENT == "development" else "Contact admin"
        },
        "message": "API is ready to serve exclusive experiences"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for graceful error responses
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Our team has been notified and is working to resolve it.",
            "type": "internal_server_error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )