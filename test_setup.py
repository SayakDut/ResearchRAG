#!/usr/bin/env python3
"""
ResearchRAG Setup Test Script
Tests that all components are properly configured and can run.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (missing)")
        return False

def check_directory_structure():
    """Check that all required directories and files exist."""
    print("🔍 Checking project structure...")
    
    required_files = [
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Documentation"),
        (".env.example", "Environment template"),
        (".gitignore", "Git ignore file"),
        ("backend/app.py", "Backend main application"),
        ("backend/requirements.txt", "Backend dependencies"),
        ("backend/Dockerfile", "Backend container config"),
        ("backend/rag_pipeline.py", "RAG implementation"),
        ("backend/summarizer.py", "AI summarization"),
        ("backend/utils/pdf_processor.py", "PDF processing"),
        ("backend/utils/url_processor.py", "URL processing"),
        ("backend/utils/exporters.py", "Export functionality"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/next.config.js", "Next.js configuration"),
        ("frontend/Dockerfile", "Frontend container config"),
        ("frontend/pages/index.tsx", "Frontend home page"),
        ("frontend/pages/paper/[id].tsx", "Paper detail page"),
        ("frontend/components/Layout.tsx", "Layout component"),
        ("frontend/components/FileUpload.tsx", "File upload component"),
        ("frontend/components/URLInput.tsx", "URL input component"),
        ("frontend/components/ChatBox.tsx", "Chat component"),
        ("frontend/lib/api.ts", "API client"),
    ]
    
    all_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_environment():
    """Check environment configuration."""
    print("\n🔧 Checking environment...")
    
    if not Path(".env").exists():
        print("⚠️  .env file not found (this is expected for first setup)")
        print("   Copy .env.example to .env and add your OpenRouter API key")
        return False
    
    # Try to load .env
    try:
        with open(".env", "r") as f:
            env_content = f.read()
        
        if "OPENROUTER_API_KEY=" in env_content:
            if "your_openrouter_api_key_here" in env_content:
                print("⚠️  Please update OPENROUTER_API_KEY in .env file")
                return False
            else:
                print("✅ OPENROUTER_API_KEY configured in .env")
                return True
        else:
            print("❌ OPENROUTER_API_KEY not found in .env")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_docker():
    """Check if Docker is available."""
    print("\n🐳 Checking Docker...")
    
    try:
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
        else:
            print("❌ Docker not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker not found or not responding")
        return False
    
    try:
        result = subprocess.run(["docker-compose", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker Compose: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker Compose not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker Compose not found")
        return False

def check_package_files():
    """Check package configuration files."""
    print("\n📦 Checking package configurations...")
    
    # Check backend requirements.txt
    try:
        with open("backend/requirements.txt", "r") as f:
            requirements = f.read()
        
        required_packages = ["fastapi", "uvicorn", "PyMuPDF", "faiss-cpu", "openai"]
        missing_packages = []
        
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing backend packages: {', '.join(missing_packages)}")
            return False
        else:
            print("✅ Backend requirements.txt looks good")
    
    except Exception as e:
        print(f"❌ Error checking backend requirements: {e}")
        return False
    
    # Check frontend package.json
    try:
        with open("frontend/package.json", "r") as f:
            package_data = json.load(f)
        
        required_deps = ["next", "react", "typescript", "tailwindcss", "axios"]
        missing_deps = []
        
        all_deps = {**package_data.get("dependencies", {}), 
                   **package_data.get("devDependencies", {})}
        
        for dep in required_deps:
            if dep not in all_deps:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"❌ Missing frontend dependencies: {', '.join(missing_deps)}")
            return False
        else:
            print("✅ Frontend package.json looks good")
            return True
    
    except Exception as e:
        print(f"❌ Error checking frontend package.json: {e}")
        return False

def main():
    """Run all setup checks."""
    print("🧪 ResearchRAG Setup Test")
    print("=" * 50)
    
    checks = [
        ("Project Structure", check_directory_structure),
        ("Package Files", check_package_files),
        ("Docker", check_docker),
        ("Environment", check_environment),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! ResearchRAG is ready to run.")
        print("\nNext steps:")
        print("1. Make sure you have an OpenRouter API key in .env")
        print("2. Run: docker-compose up --build")
        print("3. Access: http://localhost:3000")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("Refer to the README.md for detailed setup instructions.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
