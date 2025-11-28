from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from app.models import SearchQuery, SearchResponse
from app.database import get_employees_for_org
from app.utils.filters import filter_employees
from app.config import ORG_VISIBLE_COLUMNS, DEFAULT_COLUMNS
from app.rate_limiter import GLOBAL_LIMITER

router = APIRouter(tags=["search"])

def _client_id(request: Request) -> str:
    # Prefer API key header if provided; otherwise fall back to client IP
    api_key = request.headers.get("X-API-Key")
    return api_key if api_key else (request.client.host if request.client else "unknown")

def enforce_rate_limit(request: Request):
    key = _client_id(request)
    if not GLOBAL_LIMITER.allow(key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@router.get("/employees/search", response_model=SearchResponse)
def search_employees(
    request: Request,
    org_id: int = Query(..., description="Organization ID"),
    q: str | None = Query(None, description="Free-text search"),
    department: str | None = None,
    location: str | None = None,
    position: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    skills: str | None = Query(None, description="Comma-separated skill list"),
    min_years: float | None = None,
    max_years: float | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    _: None = Depends(enforce_rate_limit),
):
    # Strict org isolation first (no cross-org leakage)
    org_emps = get_employees_for_org(org_id)

    parsed_skills: List[str] | None = [s.strip() for s in skills.split(",")] if skills else None
    query = SearchQuery(
        org_id=org_id, q=q, department=department, location=location, position=position,
        email=email, phone=phone, skills=parsed_skills, min_years=min_years, max_years=max_years,
        page=page, limit=limit
    )

    # Filter within org
    filtered = filter_employees(org_emps, query)

    # Simple sort for determinism (by name)
    filtered.sort(key=lambda e: (e.name or "").lower())

    # Pagination
    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    page_items = filtered[start:end]

    # Dynamic columns per org (prevent data leak by whitelisting)
    columns = ORG_VISIBLE_COLUMNS.get(org_id, DEFAULT_COLUMNS)
    def project(e) -> Dict[str, Any]:
        payload = e.dict()
        return {k: payload.get(k) for k in columns if k in payload}

    data = [project(e) for e in page_items]

    return SearchResponse(
        data=data,
        meta={"total": total, "page": page, "limit": limit, "visible_columns": columns}
    )
