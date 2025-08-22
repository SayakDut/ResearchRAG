import fitz  # PyMuPDF
import PyPDF2
import re
from typing import Optional
from pathlib import Path

class PDFProcessor:
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF (primary) with PyPDF2 fallback."""
        try:
            return self._extract_with_pymupdf(pdf_path)
        except Exception as e:
            print(f"PyMuPDF failed: {e}, trying PyPDF2...")
            try:
                return self._extract_with_pypdf2(pdf_path)
            except Exception as e2:
                print(f"PyPDF2 also failed: {e2}")
                raise Exception(f"Failed to extract text from PDF: {e2}")
    
    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF."""
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
            text += "\n\n"  # Add page separator
        
        doc.close()
        return self._clean_text(text)
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 as fallback."""
        text = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                text += "\n\n"  # Add page separator
        
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip likely page numbers
            if re.match(r'^\d+$', line):
                continue
            
            # Skip very short lines that might be headers/footers
            if len(line) < 3:
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def extract_title(self, text: str) -> str:
        """Extract the paper title from the text."""
        lines = text.split('\n')
        
        # Look for the title in the first few lines
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            
            # Skip empty lines and very short lines
            if len(line) < 10:
                continue
            
            # Skip lines that look like headers, authors, or metadata
            if any(keyword in line.lower() for keyword in [
                'abstract', 'introduction', 'arxiv:', 'doi:', 'email:', '@',
                'university', 'department', 'conference', 'journal'
            ]):
                continue
            
            # If it's a substantial line, likely the title
            if len(line) > 15 and not line.endswith('.'):
                return line
        
        # Fallback: use the first substantial line
        for line in lines[:20]:
            line = line.strip()
            if len(line) > 15:
                return line
        
        return "Untitled Paper"
    
    def extract_metadata(self, pdf_path: str) -> dict:
        """Extract metadata from PDF."""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()
            
            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", "")
            }
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
    
    def get_page_count(self, pdf_path: str) -> int:
        """Get the number of pages in the PDF."""
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except Exception:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    return len(pdf_reader.pages)
            except Exception:
                return 0
