@echo off

REM ResearchRAG Startup Script for Windows

echo 🚀 Starting ResearchRAG...

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found!
    echo 📝 Please copy .env.example to .env and add your OpenRouter API key
    echo    copy .env.example .env
    echo    REM Then edit .env with your API key
    pause
    exit /b 1
)

echo ✅ Environment file found
echo 🐳 Starting Docker containers...

REM Start the application
docker-compose up --build

echo 🎉 ResearchRAG is running!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
pause
