from .scraper import discover_companies, extract_profile
from .scorer import score_profile
from .jobs import update_results
from .tdlr import verify_license
from models.models import ResearchJobRequest

async def run_research(job_id: str, job: ResearchJobRequest):
    urls = await discover_companies(job.trade, job.city, job.state, job.keywords)
    profiles = []
    for url in urls:
        profile = await extract_profile(url)
        if profile:
            profile.lic_active, profile.lic_number = verify_license(profile.lic_number or profile.name)
            profile.score = score_profile(profile, job)
            profiles.append(profile)
    profiles = sorted(profiles, key=lambda p: p.score, reverse=True)
    update_results(job_id, profiles[:10])
