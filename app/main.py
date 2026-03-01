from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api, pages
from app.config import settings
from app.db import Base, engine

# Create tables in actual db if running with postgres
if engine is not None:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Advanced Quantitative Market Analytics API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(api.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():
    if settings.git_sha:
        return {"git_sha": settings.git_sha}
    return {"version": "2.0.0"}
