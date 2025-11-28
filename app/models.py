from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Employee(BaseModel):
    id: int
    org_id: int
    name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    position: Optional[str] = None
    years_of_experience: Optional[float] = None
    skills: List[str] = Field(default_factory=list)

class SearchQuery(BaseModel):
    org_id: int
    q: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None  # comma-separated in query, parsed to list
    min_years: Optional[float] = None
    max_years: Optional[float] = None
    page: int = 1
    limit: int = 20

class SearchResponse(BaseModel):
    data: List[Dict[str, Any]]
    meta: Dict[str, Any]
