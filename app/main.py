
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1.router import api_router
from middleware.timing import add_process_time_header
from core.logging import setup_logging


# Configure logging once during module initialization
setup_logging()

logger = logging.getLogger("course_student_api")


# Application lifecycle manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Runs before the application starts accepting requests
    logger.info("Application startup: initializing resources.")

    try:
        yield

    finally:
        # SHUTDOWN: Runs when the application shuts down gracefully
        logger.info("Application shutdown: cleaning up resources.")


app = FastAPI(
    title="Course and Student API",
    description="API for managing courses and students",
    version="1.0.0",
    lifespan=lifespan
)


# Register middleware
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=add_process_time_header
)

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
