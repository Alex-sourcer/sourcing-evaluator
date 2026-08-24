from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os
from pathlib import Path
import uuid
from groq import Groq
from functools import lru_cache
import sqlite3
from mambu_framework import get_mambu_framework_prompt, MAMBU_LEVELS

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

client = Groq(api_key=GROQ_API_KEY)

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
    mambu_level_fit: int = None
    mambu_career_path: str = None
    mambu_level_description: str = None
    growth_potential: str = None

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
    """Use Groq API to evaluate a candidate against job description AND Mambu Career Framework"""

    prompt = f"""You are an expert talent acquisition specialist at Mambu. Evaluate this candidate.

MAMBU LEVELS: Level 8-7: Entry/Associate | Level 6: Intermediate | Level 5: Experienced | Level 4: Senior | Level 3: Advanced Senior | Level 2: Director/VP | Levels 1-0: Executive

Career Paths: IC (Individual Contributor) or TL (Team Leader)

JOB DESCRIPTION: {job_description}

CANDIDATE: {candidate.name}
Profile: {candidate.profile}

Return JSON with: match_score (0-100), technical_fit, strengths (list), red_flags (list), questions (list), recommendation (STRONG YES/YES/MAYBE/NO), reasoning, mambu_level_fit (0-8), mambu_career_path (IC or TL), growth_potential

Return ONLY JSON, no other text."""

    response = client.chat.completions.create(
        model="gemma-2-9b-it",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    try:
        # Extract and clean response text
        response_text = response.choices[0].message.content.strip()
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        response_text = response_text.strip()

        result = json.loads(response_text)
        result["candidate_name"] = candidate.name

        # Ensure Mambu fields have defaults
        if "mambu_level_fit" not in result:
            result["mambu_level_fit"] = 4
        if "mambu_career_path" not in result:
            result["mambu_career_path"] = "IC"
        if "growth_potential" not in result:
            result["growth_potential"] = "Not assessed"

        # Add Mambu level description
        level = int(result.get("mambu_level_fit", 4))
        career_path = result.get("mambu_career_path", "IC")
        if level in MAMBU_LEVELS:
            if career_path == "TL":
                result["mambu_level_description"] = MAMBU_LEVELS[level]["tl_description"]
            else:
                result["mambu_level_description"] = MAMBU_LEVELS[level]["ic_description"]

        return result
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to parse Gemini response for {candidate.name}: {str(e)}")

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
        response = client.chat.completions.create(
            model="gemma-2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        result = json.loads(response.choices[0].message.content)

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

@app.post("/api/extract-cv")
async def extract_cv(file: UploadFile = File(...)):
    """Extract candidate info from CV text file"""
    try:
        contents = await file.read()
        text_content = contents.decode('utf-8', errors='ignore')

        if not text_content.strip() or len(text_content) < 20:
            raise HTTPException(status_code=400, detail="File too short or empty")

        text_content = text_content[:2500]

        prompt = f"""Extract from this CV text only:
{{"candidate_name": "name or empty", "profile": "summary of experience in 2-3 sentences"}}

CV: {text_content}

Return ONLY JSON."""

        response = client.chat.completions.create(
            model="gemma-2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        text = response.choices[0].message.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        return {
            "success": True,
            "candidate_name": result.get("candidate_name", "").strip(),
            "profile": result.get("profile", "").strip()
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid response format")
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

@app.get("/api/admin/metrics")
async def admin_metrics():
    """Get admin dashboard metrics for reporting"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Total metrics
    c.execute("SELECT COUNT(*) FROM evaluations")
    total_evals = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT user_email) FROM evaluations WHERE user_email IS NOT NULL")
    unique_users = c.fetchone()[0]

    c.execute("SELECT AVG(CAST(json_extract(results, '$[0].match_score') AS INTEGER)) FROM evaluations")
    avg_score = c.fetchone()[0] or 0

    # Evals by user
    c.execute("""
        SELECT user_email, COUNT(*) as eval_count,
               AVG(CAST(json_extract(results, '$[0].match_score') AS INTEGER)) as avg_score
        FROM evaluations
        WHERE user_email IS NOT NULL
        GROUP BY user_email
        ORDER BY eval_count DESC
    """)
    by_user = [{"user": row[0] or "Anonymous", "evals": row[1], "avg_score": round(row[2] or 0, 1)} for row in c.fetchall()]

    # Evals by date (last 30 days)
    c.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM evaluations
        WHERE datetime(created_at) > datetime('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """)
    by_date = [{"date": row[0], "count": row[1]} for row in c.fetchall()]

    # Score distribution
    c.execute("""
        SELECT
            CASE
                WHEN CAST(json_extract(results, '$[0].match_score') AS INTEGER) >= 80 THEN '80-100'
                WHEN CAST(json_extract(results, '$[0].match_score') AS INTEGER) >= 60 THEN '60-79'
                WHEN CAST(json_extract(results, '$[0].match_score') AS INTEGER) >= 40 THEN '40-59'
                ELSE '0-39'
            END as band,
            COUNT(*) as count
        FROM evaluations
        GROUP BY band
    """)
    score_dist = {row[0]: row[1] for row in c.fetchall()}

    # Conversion metrics
    c.execute("SELECT COUNT(*) FROM candidate_outcomes WHERE hired = 1")
    total_hired = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM candidate_outcomes")
    total_tracked = c.fetchone()[0]

    conv_rate = (total_hired / total_tracked * 100) if total_tracked > 0 else 0

    # Time saved estimate (10 min per candidate screening)
    time_saved_mins = total_evals * 10
    time_saved_hours = time_saved_mins / 60

    conn.close()

    return {
        "summary": {
            "total_evaluations": total_evals,
            "unique_users": unique_users,
            "avg_match_score": round(avg_score, 1),
            "conversion_rate": round(conv_rate, 1),
            "time_saved_hours": round(time_saved_hours, 1)
        },
        "by_user": by_user,
        "by_date": by_date,
        "score_distribution": score_dist,
        "hiring_metrics": {
            "total_hired": total_hired,
            "total_tracked": total_tracked,
            "conversion_rate": round(conv_rate, 1)
        }
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
