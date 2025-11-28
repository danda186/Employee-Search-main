from fastapi import FastAPI
from app.routers.search import router as search_router

app = FastAPI(
    title="Employee Search API",
    version="1.0.0",
    description="Search-only microservice for HR employee directory with org-level dynamic columns and rate limiting."
)

app.include_router(search_router, prefix="/api/v1")
