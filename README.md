# FastAPI Subcontractor Research Agent

This is a FastAPI-based web service that accepts a subcontractor research request, performs internet searches (using Google CSE), scrapes subcontractor websites, verifies licenses using TDLR data, and returns a ranked list of relevant subcontractors.

---

## Features

- **POST /research-jobs**: Accepts job request with trade, city, and keyword context
- **GET /research-jobs/{job_id}**: Returns research results
- Scrapes and parses subcontractor profiles from the web
- License verification using TDLR CSV
- In-memory storage using a flat `database.json`
- Scoring based on license status, bonding, city match, project count

---

## Setup Instructions

### 1. Clone and navigate to the repo

```bash
git clone https://github.com/your-user/subcontractor-research-agent.git
cd subcontractor-research-agent
```

### 2. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
GOOGLE_CSE_ID=your_cse_id
DB_FILE=Your_json_filename
```

### 4. Download the file
Download the Lincenses file from [link](https://data.texas.gov/dataset/TDLR-All-Licenses/7358-krk7/about_data).
Rename the file to `TDLR_All_Licenses_20250512.csv` and put it in the services folder.

### 5. Run the server

```bash
Python main.py
```

Visit http://localhost:8000/docs to access Swagger UI.

---

## API Reference

### POST /research-jobs

Initiate a background research job.

**Request body:**

```json
{
  "trade": "mechanical",
  "city": "Austin",
  "state": "TX",
  "min_bond": 5000000,
  "keywords": ["hotel", "commercial"]
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "IN_PROGRESS"
}
```

---

### GET /research-jobs/{job_id}

Retrieve the results for a submitted research job.

---

## Project Structure

```
├── api
│   ├── __init__.py       # API package initialization
│   └── routes.py         # API routes definition
├── database
│   └── database.json     # Json file to store data
├── models
│   ├── __init__.py       # Schemas package initialization
│   └── models.py         # Schemas package initialization
└── services
    ├── __init__.py       # Services package initialization
    ├── jobs.py           # jobs definition
    ├── research.py       # research structure
    ├── scorer.py         # Scoring logic
    └── scraper.py        # scrapping of sites

─ main.py                 # Entry point of the FastAPI application
─ requirements.txt        # Project dependencies
─ README.md               # Project documentation
```
---

## Author

**Harsh**  
[LinkedIn](https://www.linkedin.com/in/harsh-9119422a8)  
[GitHub](https://github.com/Harsh6468)