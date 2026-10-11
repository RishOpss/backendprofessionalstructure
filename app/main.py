from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.v1.router import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
def home():
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