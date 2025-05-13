import uuid
import json
import os
from typing import List

import numpy as np

from models.models import ResearchJobRequest, SubcontractorProfile

DB_FILE = os.getenv("DB_FILE", "database.json")

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)

def create_job(job: ResearchJobRequest) -> str:
    job_id = str(uuid.uuid4())
    data = load_db()
    data[job_id] = {
        "status": "IN_PROGRESS",
        "results": [],
        "request": job.dict()
    }
    save_db(data)
    return job_id

def update_results(job_id: str, results: List[SubcontractorProfile]):
    data = load_db()
    data[job_id]["status"] = "SUCCEEDED"
    data[job_id]["results"] = [r.dict() for r in results]
    save_db(data)

def get_job_results(job_id: str):
    return load_db().get(job_id, {"status": "NOT_FOUND"})

def load_db():
    try:
        with open(f"database/{DB_FILE}") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(f"database/{DB_FILE}", "w") as f:
        json.dump(data, f, indent=2, cls=EnhancedJSONEncoder)
