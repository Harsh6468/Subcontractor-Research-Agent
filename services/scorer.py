from models.models import SubcontractorProfile, ResearchJobRequest

def score_profile(profile: SubcontractorProfile, job: ResearchJobRequest) -> int:
    score = 0
    if profile.lic_active:
        score += 30
    if profile.bond_amount and profile.bond_amount >= job.min_bond:
        score += 30
    if profile.city.lower() == job.city.lower():
        score += 10
    score += min(profile.tx_projects_past_5yrs * 5, 30)
    return score
