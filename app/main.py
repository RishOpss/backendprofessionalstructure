
from fastapi import FastAPI , Request
from api.v1.router import api_router
import time
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.timing import add_process_time_header
from core.logging import setup_logging
import logging

# Configure logging
setup_logging()

logger = logging.getLogger("fastapi_application")

app = FastAPI(
    title="Course and Student API",
    description="API for managing courses and students",
    version="1.0.0"
)

setup_logging()

logger = logging.getLogger("course_student_api")
logger.info("Fast API application has started.")
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
# Register all API routes
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def home():
    logger.info("Home endpoint accessed.")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Course and Student API</title>
    </head>
    <body>
        <h1>Welcome to Course and Student API</h1>
        <p>Your FastAPI application is running successfully.</p>
        <a href="/docs">Explore API Documentation</a>
    </body>
    </html>
    """

@app.get("/health", tags=["Health"])
async def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}
