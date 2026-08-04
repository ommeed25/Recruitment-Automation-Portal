from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import recruiters

from .api.linkedin import router as linkedin_router
from .api.job_sync import router as job_sync_router
from .api.jobs import router as jobs_router
from app.scheduler.scheduler import start_scheduler

app = FastAPI(
    title="LinkedIn Integration API"
)

start_scheduler()

app.include_router(linkedin_router)
app.include_router(jobs_router)
app.include_router(job_sync_router)
app.include_router(recruiters.router)

@app.get("/")
def home():
    return {
        "message": "LinkedIn Integration API is running 🚀"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

