from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
import json
from typing import Optional
import aiofiles
from pathlib import Path

from rag_pipeline import RAGPipeline
from summarizer import PaperSummarizer
from utils.pdf_processor import PDFProcessor
from utils.url_processor import URLProcessor

app = FastAPI(title="ResearchRAG API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
rag_pipeline = RAGPipeline()
summarizer = PaperSummarizer()
pdf_processor = PDFProcessor()
url_processor = URLProcessor()

# Data storage
UPLOAD_DIR = Path("uploads")
DATA_DIR = Path("data")
UPLOAD_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    query: str

class PaperResponse(BaseModel):
    paper_id: str
    title: str
    summary: str
    pros: list[str]
    cons: list[str]
    future_work: list[str]

@app.get("/")
async def root():
    return {"message": "ResearchRAG API is running"}

@app.post("/upload-paper")
async def upload_paper(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None)
):
    """Upload a PDF file or provide a URL to process a research paper."""
    if not file and not url:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided")
    
    paper_id = str(uuid.uuid4())
    
    try:
        if file:
            # Handle file upload
            file_path = UPLOAD_DIR / f"{paper_id}.pdf"
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Extract text from PDF
            text_content = pdf_processor.extract_text(str(file_path))
            title = pdf_processor.extract_title(text_content)
            
        else:
            # Handle URL
            text_content, title = url_processor.process_url(url)
        
        # Store paper data
        paper_data = {
            "paper_id": paper_id,
            "title": title,
            "content": text_content,
            "source": file.filename if file else url
        }
        
        # Save paper data
        data_file = DATA_DIR / f"{paper_id}.json"
        async with aiofiles.open(data_file, 'w') as f:
            await f.write(json.dumps(paper_data, indent=2))
        
        # Process with RAG pipeline
        rag_pipeline.add_document(paper_id, text_content)
        
        # Generate summary
        summary_data = summarizer.generate_summary(text_content)
        
        # Update paper data with summary
        paper_data.update(summary_data)
        async with aiofiles.open(data_file, 'w') as f:
            await f.write(json.dumps(paper_data, indent=2))
        
        return {
            "paper_id": paper_id,
            "title": title,
            "message": "Paper processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing paper: {str(e)}")

@app.get("/summary/{paper_id}")
async def get_summary(paper_id: str):
    """Get the summary, pros/cons, and future work for a paper."""
    data_file = DATA_DIR / f"{paper_id}.json"
    
    if not data_file.exists():
        raise HTTPException(status_code=404, detail="Paper not found")
    
    try:
        async with aiofiles.open(data_file, 'r') as f:
            content = await f.read()
            paper_data = json.loads(content)
        
        return PaperResponse(
            paper_id=paper_data["paper_id"],
            title=paper_data["title"],
            summary=paper_data.get("summary", ""),
            pros=paper_data.get("pros", []),
            cons=paper_data.get("cons", []),
            future_work=paper_data.get("future_work", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving summary: {str(e)}")

@app.post("/chat/{paper_id}")
async def chat_with_paper(paper_id: str, request: ChatRequest):
    """Chat with a paper using RAG."""
    data_file = DATA_DIR / f"{paper_id}.json"
    
    if not data_file.exists():
        raise HTTPException(status_code=404, detail="Paper not found")
    
    try:
        response = rag_pipeline.query(paper_id, request.query)
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/export/{paper_id}/{format}")
async def export_summary(paper_id: str, format: str):
    """Export paper summary as PDF or Markdown."""
    if format not in ["pdf", "markdown"]:
        raise HTTPException(status_code=400, detail="Format must be 'pdf' or 'markdown'")
    
    data_file = DATA_DIR / f"{paper_id}.json"
    
    if not data_file.exists():
        raise HTTPException(status_code=404, detail="Paper not found")
    
    try:
        async with aiofiles.open(data_file, 'r') as f:
            content = await f.read()
            paper_data = json.loads(content)
        
        if format == "markdown":
            from utils.exporters import MarkdownExporter
            exporter = MarkdownExporter()
            file_path = exporter.export(paper_data)
            return FileResponse(
                file_path,
                media_type="text/markdown",
                filename=f"{paper_data['title']}.md"
            )
        else:
            from utils.exporters import PDFExporter
            exporter = PDFExporter()
            file_path = exporter.export(paper_data)
            return FileResponse(
                file_path,
                media_type="application/pdf",
                filename=f"{paper_data['title']}.pdf"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
