import os
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from models.models import SubcontractorProfile

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

async def discover_companies(trade, city, state, keywords):
    query = f"{trade} subcontractor from the {city} {state} " + " ".join(keywords)
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": 10
    }

    urls = set()
    async with httpx.AsyncClient() as client:
        for start in [1, 11, 21]:
            params["start"] = start
            res = await client.get(url, params=params)
            if res.status_code != 200:
                continue
            results = res.json().get("items", [])
            for item in results:
                link = item.get("link")
                if link and link.startswith("http"):
                    urls.add(link)
            if len(urls) >= 20:
                break

    return list(urls)[:20]


def extract_field(text, patterns):
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return str(match.group())
    return None

async def extract_profile(url: str) -> SubcontractorProfile:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        profile = SubcontractorProfile(
            name=soup.title.string.strip() if soup.title else "Unknown",
            website=url,
            city="Austin",
            state="TX",
            lic_active=None,
            lic_number=extract_field(text, [r"TX\d{6,}", r"#\d{6,}"]),
            bond_amount=parse_bond(text),
            tx_projects_past_5yrs=parse_projects(text),
            phone_number=extract_field(text, [r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"]),
            email=extract_field(text, [r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"]),
            score=0,
            evidence_url=url,
            evidence_text=extract_field(text, [r"[Bb]onded.*?\$", r"[Pp]rojects.*?Texas"]),
            last_checked=datetime.utcnow().isoformat()
        )
        return profile
    except:
        return None

def parse_bond(text):
    match = re.search(r"(bonded\s+up\s+to\s+\$?(\d+[\d,]*))", text, re.IGNORECASE)
    if match:
        digits = re.sub(r"[^\d]", "", match.group(2))
        return int(digits)
    return None

def parse_projects(text):
    return len(re.findall(r"(20[1-2][0-9]).*?(Texas|TX)", text, re.IGNORECASE))
