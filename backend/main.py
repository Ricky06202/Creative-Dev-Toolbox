from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import auth, tools, favorites
from fastapi.responses import JSONResponse
import traceback

# FastAPI App
app = FastAPI(title="Creative Dev-Toolbox API")

# Explicit initialization for WSGI/cPanel stability
try:
    create_db_and_tables()
except Exception as e:
    print(f"Error initializing database: {e}")

# Global Exception Handler for Debugging (Crucial for 500 errors in cPanel)
@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc()
        },
        headers={
            "Access-Control-Allow-Origin": "https://creativedevtool.rsanjur.com",
            "Access-Control-Allow-Credentials": "true"
        }
    )

# Configure CORS
origins = [
    "https://creativedevtool.rsanjur.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(tools.router)
app.include_router(favorites.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Creative Dev-Toolbox API (Modular Version)"}
