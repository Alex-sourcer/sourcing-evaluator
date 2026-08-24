from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os
from pathlib import Path
import uuid
import google.generativeai as genai
from functools import lru_cache
import sqlite3

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)

DB_PATH = Path("evaluations.db")

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id TEXT PRIMARY KEY,
            job_description TEXT NOT NULL,
            candidates TEXT NOT NULL,
            results TEXT NOT NULL,
            created_at TEXT NOT NULL,
            share_token TEXT UNIQUE,
            user_email TEXT,
            department TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidate_searches (
            id TEXT PRIMARY KEY,
            job_description TEXT NOT NULL,
            search_results TEXT NOT NULL,
            created_at TEXT NOT NULL,
            user_email TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidate_outcomes (
            id TEXT PRIMARY KEY,
            candidate_name TEXT NOT NULL,
            match_score INTEGER,
            hired BOOLEAN,
            hired_at TEXT,
            evaluation_id TEXT,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS google_sheets_exports (
            id TEXT PRIMARY KEY,
            spreadsheet_id TEXT,
            exported_at TEXT,
            record_count INTEGER,
            user_email TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Candidate(BaseModel):
    name: str
    profile: str
    linkedin: str = ""

class EvaluationRequest(BaseModel):
    job_description: str
    candidates: list[Candidate]
    user_email: str = None
    department: str = None

class EvaluationResult(BaseModel):
    candidate_name: str
    match_score: int
    technical_fit: str
    strengths: list[str]
    red_flags: list[str]
    questions: list[str]
    recommendation: str
    reasoning: str

def save_evaluation(job_desc: str, candidates: list[Candidate], results: list[dict], user_email: str = None):
    """Save evaluation to database"""
    eval_id = str(uuid.uuid4())
    share_token = str(uuid.uuid4())[:8]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO evaluations (id, job_description, candidates, results, created_at, share_token, user_email) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (eval_id, job_desc, json.dumps([cand.dict() for cand in candidates]), json.dumps(results), datetime.now().isoformat(), share_token, user_email)
    )
    conn.commit()
    conn.close()

    return eval_id, share_token

def get_evaluation(eval_id: str):
    """Retrieve evaluation from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT job_description, candidates, results, created_at FROM evaluations WHERE id = ?", (eval_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "job_description": row[0],
        "candidates": json.loads(row[1]),
        "results": json.loads(row[2]),
        "created_at": row[3]
    }

def evaluate_with_gemini(job_description: str, candidate: Candidate) -> dict:
    """Use Gemini API to evaluate a candidate against job description"""
    prompt = f"""
You are an expert talent acquisition specialist. Evaluate this candidate against the job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
Name: {candidate.name}
Profile: {candidate.profile}
LinkedIn: {candidate.linkedin if candidate.linkedin else "Not provided"}

Provide a comprehensive evaluation in JSON format with these exact fields:
- match_score (0-100, percentage)
- technical_fit (one sentence summary)
- strengths (list of 3-4 key strengths)
- red_flags (list of 2-3 concerns or gaps, or empty list if none)
- questions (list of 3 clarifying questions to ask in interview)
- recommendation (STRONG YES, YES, MAYBE, or NO)
- reasoning (2-3 sentences explaining the recommendation)

Return ONLY valid JSON, no additional text.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        result = json.loads(response.text)
        result["candidate_name"] = candidate.name
        return result
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse Gemini response for {candidate.name}")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/api/evaluate")
async def evaluate_candidates(request: EvaluationRequest, background_tasks: BackgroundTasks):
    """Evaluate multiple candidates against job description"""
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if not request.candidates:
        raise HTTPException(status_code=400, detail="At least one candidate is required")

    try:
        results = []
        for candidate in request.candidates:
            result = evaluate_with_gemini(request.job_description, candidate)
            results.append(result)

        eval_id, share_token = save_evaluation(
            request.job_description,
            request.candidates,
            results,
            user_email=request.user_email
        )

        # Update evaluation with department if provided
        if request.department:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE evaluations SET department = ? WHERE id = ?", (request.department, eval_id))
            conn.commit()
            conn.close()

        return {
            "success": True,
            "evaluation_id": eval_id,
            "share_token": share_token,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/evaluation/{eval_id}")
async def get_saved_evaluation(eval_id: str):
    """Retrieve a saved evaluation"""
    data = get_evaluation(eval_id)
    if not data:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return data

@app.get("/api/share/{share_token}")
async def get_shared_evaluation(share_token: str):
    """Retrieve evaluation by share token"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, job_description, candidates, results, created_at FROM evaluations WHERE share_token = ?", (share_token,))
    row = c.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return {
        "id": row[0],
        "job_description": row[1],
        "candidates": json.loads(row[2]),
        "results": json.loads(row[3]),
        "created_at": row[4]
    }

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get analytics for dashboard"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM evaluations")
    total_evals = c.fetchone()[0]

    c.execute("""
        SELECT user_email, COUNT(*) as count
        FROM evaluations
        WHERE user_email IS NOT NULL
        GROUP BY user_email
        ORDER BY count DESC
    """)
    evals_by_user = [{"email": row[0], "count": row[1]} for row in c.fetchall()]

    c.execute("""
        SELECT
            DATE(created_at) as date,
            COUNT(*) as count
        FROM evaluations
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 30
    """)
    evals_by_date = [{"date": row[0], "count": row[1]} for row in c.fetchall()]

    c.execute("""
        SELECT department, COUNT(*) as count
        FROM evaluations
        WHERE department IS NOT NULL
        GROUP BY department
    """)
    evals_by_dept = [{"department": row[0], "count": row[1]} for row in c.fetchall()]

    c.execute("""
        SELECT results FROM evaluations WHERE results IS NOT NULL LIMIT 100
    """)
    all_results = []
    for row in c.fetchall():
        try:
            results = json.loads(row[0])
            all_results.extend(results)
        except:
            pass

    avg_score = sum(r.get("match_score", 0) for r in all_results) / len(all_results) if all_results else 0

    recommendation_counts = {}
    for r in all_results:
        rec = r.get("recommendation", "UNKNOWN")
        recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1

    conn.close()

    return {
        "total_evaluations": total_evals,
        "avg_match_score": round(avg_score, 1),
        "evaluations_by_user": evals_by_user,
        "evaluations_by_date": evals_by_date,
        "evaluations_by_department": evals_by_dept,
        "recommendation_distribution": recommendation_counts
    }

@app.post("/api/search-candidates")
async def search_candidates(request: EvaluationRequest):
    """AI-powered candidate search based on job description"""
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description required")

    prompt = f"""
Based on this job description, suggest 5-7 ideal LinkedIn search strings to find matching candidates.

JOB DESCRIPTION:
{request.job_description}

Return a JSON object with this structure:
{{
    "search_queries": [
        {{"query": "example query", "description": "what this finds"}},
        ...
    ],
    "search_tips": ["tip 1", "tip 2", ...],
    "ideal_profile": "2-3 sentence description of ideal candidate"
}}

Return ONLY valid JSON, no additional text.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        result = json.loads(response.text)

        search_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO candidate_searches (id, job_description, search_results, created_at) VALUES (?, ?, ?, ?)",
            (search_id, request.job_description, json.dumps(result), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        return {
            "success": True,
            "search_id": search_id,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/candidate-outcome")
async def record_candidate_outcome(
    candidate_name: str,
    match_score: int,
    hired: bool,
    evaluation_id: str = None
):
    """Record if a candidate was hired or not (for conversion tracking)"""
    outcome_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidate_outcomes
        (id, candidate_name, match_score, hired, hired_at, evaluation_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        outcome_id,
        candidate_name,
        match_score,
        hired,
        datetime.now().isoformat() if hired else None,
        evaluation_id,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    return {"success": True, "outcome_id": outcome_id}

@app.get("/api/conversion-analytics")
async def get_conversion_analytics():
    """Analyze conversion rates and predict hiring likelihood"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT match_score, hired, COUNT(*) as count
        FROM candidate_outcomes
        GROUP BY match_score, hired
        ORDER BY match_score DESC
    """)

    score_outcomes = {}
    total_hired = 0
    total_evaluated = 0

    for row in c.fetchall():
        score, hired, count = row[0], row[1], row[2]
        total_evaluated += count
        if hired:
            total_hired += count

        if score not in score_outcomes:
            score_outcomes[score] = {"hired": 0, "not_hired": 0}

        if hired:
            score_outcomes[score]["hired"] = count
        else:
            score_outcomes[score]["not_hired"] = count

    # Calculate conversion rate by score band
    conversion_by_band = {}
    bands = [
        (80, 100, "80-100%"),
        (60, 79, "60-79%"),
        (40, 59, "40-59%"),
        (0, 39, "0-39%")
    ]

    for min_score, max_score, label in bands:
        c.execute("""
            SELECT COUNT(CASE WHEN hired THEN 1 END) as hired,
                   COUNT(*) as total
            FROM candidate_outcomes
            WHERE match_score >= ? AND match_score <= ?
        """, (min_score, max_score))

        hired_count, total_count = c.fetchone()
        if total_count > 0:
            conversion_rate = (hired_count / total_count) * 100
            conversion_by_band[label] = {
                "hired": hired_count or 0,
                "total": total_count or 0,
                "conversion_rate": round(conversion_rate, 1)
            }

    # Overall metrics
    overall_rate = (total_hired / total_evaluated * 100) if total_evaluated > 0 else 0

    conn.close()

    return {
        "overall_conversion_rate": round(overall_rate, 1),
        "total_evaluated": total_evaluated,
        "total_hired": total_hired,
        "conversion_by_score_band": conversion_by_band,
        "score_details": score_outcomes
    }

@app.post("/api/export-google-sheets")
async def export_to_google_sheets():
    """Export all evaluations to Google Sheets"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Get all evaluations
        c.execute("""
            SELECT id, job_description, candidates, results, created_at, user_email, department
            FROM evaluations
            ORDER BY created_at DESC
        """)

        evaluations = []
        for row in c.fetchall():
            eval_id, job_desc, candidates, results, created_at, user_email, dept = row
            try:
                results_list = json.loads(results)
                for result in results_list:
                    evaluations.append({
                        "evaluation_id": eval_id,
                        "candidate_name": result.get("candidate_name", ""),
                        "match_score": result.get("match_score", 0),
                        "technical_fit": result.get("technical_fit", ""),
                        "recommendation": result.get("recommendation", ""),
                        "strengths": "; ".join(result.get("strengths", [])),
                        "red_flags": "; ".join(result.get("red_flags", [])),
                        "job_description": job_desc[:100],
                        "created_at": created_at,
                        "evaluated_by": user_email or "unknown",
                        "department": dept or "unassigned"
                    })
            except:
                pass

        # Format for CSV (as fallback since we can't use Google Sheets API without auth)
        # In production, integrate with Google Sheets API
        export_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO google_sheets_exports
            (id, spreadsheet_id, exported_at, record_count, user_email)
            VALUES (?, ?, ?, ?, ?)
        """, (export_id, "local-export", datetime.now().isoformat(), len(evaluations), "system"))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "export_id": export_id,
            "records": evaluations,
            "count": len(evaluations),
            "note": "Exportar a CSV o Google Sheets manualmente desde esta data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
