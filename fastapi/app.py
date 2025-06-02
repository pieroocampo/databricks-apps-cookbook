"""
Main FastAPI application.

This module creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from fastapi import FastAPI

from routes import api_router
from services.db.connector import close_connections
from errors.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup code (if any)
    yield
    # Shutdown code
    close_connections()


# Create the main FastAPI application
app = FastAPI(
    title="FastAPI & Databricks Apps",
    description="A simple FastAPI application example for Databricks Apps runtime",
    version="1.0.0",
    lifespan=lifespan,
)

# Register exception handlers
register_exception_handlers(app)

# Include the API router
app.include_router(api_router)


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "app": "Databricks FastAPI Example",
        "message": "Welcome to the Databricks FastAPI example app",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=1200)
