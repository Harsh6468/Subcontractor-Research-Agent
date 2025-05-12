from fastapi import APIRouter, BackgroundTasks
from models.models import ResearchJobRequest
from services.jobs import create_job, get_job_results
from services.research import run_research


router = APIRouter()

@router.post("/research-jobs")
def submit_job(job: ResearchJobRequest, background_tasks: BackgroundTasks):
    job_id = create_job(job)
    background_tasks.add_task(run_research, job_id, job)
    return {"job_id": job_id, "status": "IN_PROGRESS"}

@router.get("/research-jobs/{job_id}")
def get_results(job_id: str):
    return get_job_results(job_id)
