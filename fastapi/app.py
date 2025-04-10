from typing import Dict

import uvicorn
from fastapi import FastAPI

from routes import api_router


# Create the main FastAPI application
app = FastAPI(
    title="FastAPI & Databricks Apps",
    description="A simple FastAPI application example for Databricks Apps runtime",
    version="1.0.0",
)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
