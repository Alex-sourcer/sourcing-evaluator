#!/usr/bin/env python3
"""
Quick health check script for Sourcing Evaluator
Run this to verify everything is set up correctly
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python 3.10+"""
    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_env_file():
    """Check if .env exists and has API key"""
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("   Create it with: cp .env.example .env")
        return False

    with open(".env", "r") as f:
        content = f.read()
        if "GEMINI_API_KEY=" not in content:
            print("❌ GEMINI_API_KEY not found in .env")
            return False
        if content.split("GEMINI_API_KEY=")[1].split("\n")[0].strip() == "your_api_key_here":
            print("⚠️  GEMINI_API_KEY is still set to placeholder")
            return False

    print("✅ .env file exists with API key")
    return True

def check_dependencies():
    """Check if all required packages can be imported"""
    required = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "google.generativeai": "Google Generative AI",
        "dotenv": "python-dotenv"
    }

    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not installed")
            print(f"   Run: pip install -r requirements.txt")
            all_ok = False

    return all_ok

def check_files():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "static/index.html",
        "static/style.css",
        "static/script.js",
        "Procfile",
        ".env"
    ]

    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_ok = False

    return all_ok

def check_gemini_api():
    """Test connection to Gemini API"""
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not set in environment")
            return False

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'test success' in one word")

        if response.text:
            print("✅ Gemini API connection successful")
            return True
        else:
            print("⚠️  Gemini API responded but no text")
            return True
    except Exception as e:
        print(f"❌ Gemini API error: {str(e)}")
        print("   Check your API key at https://ai.google.dev")
        return False

def main():
    print("\n🏥 Sourcing Evaluator - Health Check")
    print("=" * 40)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Required Files", check_files),
        ("Dependencies", check_dependencies),
        ("Gemini API", check_gemini_api),
    ]

    results = []
    for name, check in checks:
        print(f"\n{name}:")
        print("-" * 40)
        results.append((name, check()))

    print("\n" + "=" * 40)
    print("Summary:")
    print("=" * 40)

    all_ok = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_ok = False

    print("\n" + "=" * 40)
    if all_ok:
        print("✅ Everything looks good!")
        print("\nTo start the app, run:")
        print("  python app.py")
        print("\nThen open: http://localhost:8000")
    else:
        print("⚠️  Some checks failed. See above for details.")
        print("\nCommon fixes:")
        print("1. API key: Get one from https://ai.google.dev")
        print("2. Dependencies: pip install -r requirements.txt")
        print("3. Python: Use Python 3.10 or higher")

    print()
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
