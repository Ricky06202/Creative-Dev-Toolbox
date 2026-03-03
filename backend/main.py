from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import auth, tools, favorites

# FastAPI App
app = FastAPI(title="Creative Dev-Toolbox API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
