#!/bin/bash

# ResearchRAG Startup Script

echo "🚀 Starting ResearchRAG..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.example to .env and add your OpenRouter API key"
    echo "   cp .env.example .env"
    echo "   # Then edit .env with your API key"
    exit 1
fi

# Check if OPENROUTER_API_KEY is set
source .env
if [ -z "$OPENROUTER_API_KEY" ] || [ "$OPENROUTER_API_KEY" = "your_openrouter_api_key_here" ]; then
    echo "❌ OPENROUTER_API_KEY not set in .env file!"
    echo "📝 Please edit .env and add your OpenRouter API key"
    echo "   Get your free API key from: https://openrouter.ai/"
    exit 1
fi

echo "✅ Environment configured"
echo "🐳 Starting Docker containers..."

# Start the application
docker-compose up --build

echo "🎉 ResearchRAG is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
