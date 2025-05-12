from pydantic import BaseModel
from typing import List, Optional

class ResearchJobRequest(BaseModel):
    trade: str
    city: str
    state: str
    min_bond: int
    keywords: Optional[List[str]] = []

class SubcontractorProfile(BaseModel):
    name: str
    website: str
    city: Optional[str]
    state: Optional[str]
    lic_active: Optional[bool]
    lic_number: Optional[str]
    bond_amount: Optional[int]
    tx_projects_past_5yrs: Optional[int]
    score: int
    evidence_url: Optional[str]
    evidence_text: Optional[str]
    last_checked: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]

class JobResult(BaseModel):
    status: str
    results: List[SubcontractorProfile] = []
