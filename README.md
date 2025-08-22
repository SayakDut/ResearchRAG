# ResearchRAG

A complete end-to-end production-ready application for research paper analysis using RAG (Retrieval-Augmented Generation).

## 🚀 Features

- **📄 Paper Upload**: Upload PDF files or provide URLs (arXiv, direct PDF links)
- **🤖 AI Analysis**: Generate comprehensive summaries, pros/cons, and future work suggestions
- **💬 Interactive Chat**: Ask questions about papers using RAG technology
- **📊 Export Options**: Export summaries as PDF or Markdown
- **🐳 Docker Ready**: Production-ready containerized deployment
- **🆓 Free AI Models**: Uses only free OpenRouter models

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python 3.11
- **AI**: OpenRouter API (`openai/gpt-oss-20b:free`)
- **Vector DB**: FAISS (free, local)
- **PDF Processing**: PyMuPDF + PyPDF2
- **Deployment**: Docker + Docker Compose

## ⚡ Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenRouter API key (free at [openrouter.ai](https://openrouter.ai/))

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ResearchRAG
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### 2. Start the Application

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

**Manual Docker:**
```bash
export OPENROUTER_API_KEY=your_api_key_here
docker-compose up --build
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
researchrag/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main FastAPI application
│   ├── rag_pipeline.py     # RAG implementation with FAISS
│   ├── summarizer.py       # AI summarization logic
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Backend container
│   └── utils/             # Utility modules
│       ├── pdf_processor.py    # PDF text extraction
│       ├── url_processor.py    # URL/arXiv processing
│       └── exporters.py        # PDF/Markdown export
├── frontend/               # Next.js frontend
│   ├── pages/             # Next.js pages
│   ├── components/        # React components
│   ├── lib/              # API client
│   ├── styles/           # Tailwind CSS
│   ├── package.json      # Node dependencies
│   └── Dockerfile        # Frontend container
├── docker-compose.yml     # Container orchestration
├── .env.example          # Environment template
└── README.md            # This file
```

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload-paper` | Upload PDF file or URL |
| `GET` | `/summary/{paper_id}` | Get paper analysis |
| `POST` | `/chat/{paper_id}` | Chat with paper |
| `GET` | `/export/{paper_id}/{format}` | Export summary (pdf/markdown) |

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | ✅ Yes |

## 🎯 Usage Examples

### 1. Upload a PDF
- Go to http://localhost:3000
- Drag and drop a PDF file or click to select
- Wait for AI analysis to complete
- View summary, pros/cons, and future work

### 2. Process arXiv Paper
- Click "Paper URL" tab
- Enter: `https://arxiv.org/abs/2301.00001`
- Click "Analyze Paper"
- Interact with the results

### 3. Chat with Paper
- After uploading, click the "Chat" tab
- Ask questions like:
  - "What is the main contribution?"
  - "What are the limitations?"
  - "How does this compare to previous work?"

## 🚨 Troubleshooting

### Common Issues

**1. "OPENROUTER_API_KEY not set"**
- Copy `.env.example` to `.env`
- Add your API key from [openrouter.ai](https://openrouter.ai/)

**2. Docker build fails**
- Ensure Docker is running
- Try: `docker-compose down && docker-compose up --build`

**3. PDF upload fails**
- Check file size (max 50MB)
- Ensure PDF is not password-protected
- Try a different PDF file

**4. Frontend can't connect to backend**
- Ensure both containers are running
- Check `docker-compose logs backend`
- Verify ports 3000 and 8000 are available

## 🧪 Testing

The application includes comprehensive error handling and validation:

- **File validation**: PDF format and size checks
- **URL validation**: Supports arXiv and direct PDF URLs
- **API error handling**: Graceful degradation on AI service issues
- **Health checks**: Docker container monitoring

## 🔒 Security Notes

- API keys are handled securely through environment variables
- File uploads are validated and stored safely
- No sensitive data is logged
- CORS is properly configured

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker logs: `docker-compose logs`
3. Open an issue on GitHub

---

**Built with ❤️ using free AI models and open-source technologies**
