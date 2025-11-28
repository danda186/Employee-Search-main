# app/database.py
"""
In-memory mock "database" that auto-seeds fake employees for testing.
No external libraries — all stdlib only.
"""

import random
from typing import List, Dict
from app.models import Employee

_EMPLOYEES: List[Employee] = []
_BY_ORG: Dict[int, List[Employee]] = {}

FIRST_NAMES = [
    "John", "Jane", "Alex", "Emily", "Michael", "Sarah", "Robert", "Olivia",
    "Daniel", "Sophia", "William", "Ava", "James", "Emma", "David", "Mia"
]
LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore",
    "Taylor", "Anderson", "Thomas", "Jackson", "White"
]
DEPARTMENTS = ["HR", "Engineering", "Sales", "Marketing", "Finance", "Support"]
LOCATIONS = ["New York", "San Francisco", "London", "Berlin", "Singapore"]
POSITIONS = ["Manager", "Engineer", "Analyst", "Designer", "Intern", "Director"]
SKILLS = ["python", "excel", "fastapi", "salesforce", "sql", "aws", "react", "django"]

def _random_employee(emp_id: int, org_id: int) -> Employee:
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    email = f"{name.lower().replace(' ', '.')}@org{org_id}.com"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    department = random.choice(DEPARTMENTS)
    location = random.choice(LOCATIONS)
    position = random.choice(POSITIONS)
    years = round(random.uniform(1, 15), 1)
    skills = random.sample(SKILLS, k=random.randint(2, 5))
    return Employee(
        id=emp_id,
        org_id=org_id,
        name=name,
        email=email,
        phone=phone,
        department=department,
        location=location,
        position=position,
        years_of_experience=years,
        skills=skills
    )

def _seed(num_orgs: int = 3, per_org: int = 200):
    """Auto-generate mock data for all orgs"""
    global _EMPLOYEES, _BY_ORG
    emp_id = 1
    for org_id in range(1, num_orgs + 1):
        org_emps = []
        for _ in range(per_org):
            emp = _random_employee(emp_id, org_id)
            _EMPLOYEES.append(emp)
            org_emps.append(emp)
            emp_id += 1
        _BY_ORG[org_id] = org_emps
    print(f"[INFO] Seeded {_EMPLOYEES.__len__()} mock employees across {num_orgs} orgs.")

# Automatically seed data at import time
_seed()

def get_employees_for_org(org_id: int) -> List[Employee]:
    """Retrieve employees for the given organization."""
    return _BY_ORG.get(org_id, [])
