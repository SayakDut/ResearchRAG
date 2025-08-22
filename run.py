#!/usr/bin/env python3
"""
Simple script to run ResearchRAG locally
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    print("🚀 Starting ResearchRAG...")

    # Load environment variables from .env
    if Path(".env").exists():
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        print("✅ Environment loaded")
    else:
        print("⚠️  .env file not found, using system environment")

    # Set API key in environment
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found. Please set it in .env file.")
        return 1

    print("🐍 Starting backend on http://localhost:8000")
    print("📖 API docs will be at http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")

    # Start backend with environment variable
    try:
        subprocess.run([
            "python", "-m", "uvicorn", "app:app",
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], cwd="backend", env=os.environ)
    except KeyboardInterrupt:
        print("\n🛑 Stopping backend...")
        return 0

if __name__ == "__main__":
    sys.exit(main())
