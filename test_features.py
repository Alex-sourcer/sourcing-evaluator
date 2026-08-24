#!/usr/bin/env python3
"""
Test script to verify all features work correctly
Run after deploying to test API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test basic health check"""
    print("\n✓ Testing health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("  ✓ Health check passed")

def test_search_candidates():
    """Test candidate search feature"""
    print("\n✓ Testing candidate search...")
    payload = {
        "job_description": "Senior Python Developer with Django and PostgreSQL experience",
        "candidates": []
    }

    response = requests.post(f"{BASE_URL}/api/search-candidates", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "search_queries" in data["data"]
    print(f"  ✓ Generated {len(data['data']['search_queries'])} search queries")

def test_evaluation():
    """Test evaluation feature"""
    print("\n✓ Testing candidate evaluation...")
    payload = {
        "job_description": "Senior Backend Engineer - Python, FastAPI, PostgreSQL, AWS",
        "candidates": [
            {
                "name": "Juan García",
                "profile": "5 años Python, Django/FastAPI, PostgreSQL, AWS expert",
                "linkedin": "linkedin.com/in/juan"
            },
            {
                "name": "María López",
                "profile": "3 años backend, Java + Python, some AWS experience",
                "linkedin": "linkedin.com/in/maria"
            }
        ],
        "user_email": "test@example.com",
        "department": "Backend Engineering"
    }

    response = requests.post(f"{BASE_URL}/api/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["results"]) == 2
    assert "match_score" in data["results"][0]
    assert "recommendation" in data["results"][0]
    print(f"  ✓ Evaluated {len(data['results'])} candidates")
    for result in data["results"]:
        print(f"    - {result['candidate_name']}: {result['match_score']}%")

def test_dashboard():
    """Test dashboard stats"""
    print("\n✓ Testing dashboard analytics...")
    response = requests.get(f"{BASE_URL}/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_evaluations" in data
    assert "avg_match_score" in data
    assert "evaluations_by_user" in data
    print(f"  ✓ Total evaluations: {data['total_evaluations']}")
    print(f"  ✓ Avg match score: {data['avg_match_score']}%")

def test_conversion_analytics():
    """Test conversion prediction"""
    print("\n✓ Testing conversion analytics...")
    response = requests.get(f"{BASE_URL}/api/conversion-analytics")
    assert response.status_code == 200
    data = response.json()
    assert "overall_conversion_rate" in data
    assert "conversion_by_score_band" in data
    print(f"  ✓ Overall conversion rate: {data['overall_conversion_rate']}%")
    print(f"  ✓ Score bands analyzed")

def test_export_sheets():
    """Test Google Sheets export"""
    print("\n✓ Testing export to Sheets...")
    response = requests.post(f"{BASE_URL}/api/export-google-sheets")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "records" in data
    assert data["count"] > 0
    print(f"  ✓ Exported {data['count']} records")

def test_outcome_tracking():
    """Test outcome/hiring tracking"""
    print("\n✓ Testing outcome tracking...")
    payload = {
        "candidate_name": "Test Candidate",
        "match_score": 78,
        "hired": True,
        "evaluation_id": "test-eval-123"
    }

    response = requests.post(f"{BASE_URL}/api/candidate-outcome", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"  ✓ Outcome recorded: {payload['candidate_name']} hired={payload['hired']}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("🧪 Sourcing Evaluator - Feature Tests")
    print("="*50)

    tests = [
        ("Health Check", test_health),
        ("Candidate Search", test_search_candidates),
        ("Candidate Evaluation", test_evaluation),
        ("Dashboard Analytics", test_dashboard),
        ("Conversion Prediction", test_conversion_analytics),
        ("Export to Sheets", test_export_sheets),
        ("Outcome Tracking", test_outcome_tracking),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ❌ {test_name} failed: {str(e)}")
            failed += 1

    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")

    if failed == 0:
        print("✅ All tests passed! App is ready to use.")
    else:
        print(f"❌ {failed} test(s) failed. Check the output above.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at", BASE_URL)
        print("Make sure the app is running: python app.py")
