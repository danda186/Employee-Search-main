from typing import Iterable, List
from app.models import Employee, SearchQuery

def _matches_text(emp: Employee, q: str) -> bool:
    text = " ".join([
        emp.name or "", emp.email or "", emp.phone or "",
        emp.department or "", emp.location or "", emp.position or "",
        " ".join(emp.skills or [])
    ]).lower()
    return q.lower() in text

def _skills_include(emp: Employee, required: List[str]) -> bool:
    if not required:
        return True
    s = set((emp.skills or []))
    return all(sk in s for sk in required)

def filter_employees(candidates: Iterable[Employee], query: SearchQuery) -> List[Employee]:
    out = []
    for e in candidates:
        if query.q and not _matches_text(e, query.q):
            continue
        if query.department and (e.department or "").lower() != query.department.lower():
            continue
        if query.location and (e.location or "").lower() != query.location.lower():
            continue
        if query.position and (e.position or "").lower() != query.position.lower():
            continue
        if query.email and (e.email or "").lower() != query.email.lower():
            continue
        if query.phone and (e.phone or "").lower() != query.phone.lower():
            continue
        if query.skills and not _skills_include(e, query.skills):
            continue
        if query.min_years is not None and (e.years_of_experience or 0) < query.min_years:
            continue
        if query.max_years is not None and (e.years_of_experience or 0) > query.max_years:
            continue
        out.append(e)
    return out
