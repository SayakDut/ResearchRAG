import requests
import re
from typing import Tuple
from urllib.parse import urlparse
import tempfile
import os

class URLProcessor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def process_url(self, url: str) -> Tuple[str, str]:
        """Process a URL and extract paper content."""
        # Check if it's an arXiv URL
        if 'arxiv.org' in url:
            return self._process_arxiv_url(url)
        
        # Check if it's a direct PDF URL
        if url.lower().endswith('.pdf'):
            return self._process_pdf_url(url)
        
        # Try to extract text from web page
        return self._process_web_page(url)
    
    def _process_arxiv_url(self, url: str) -> Tuple[str, str]:
        """Process arXiv URLs to get PDF content."""
        # Convert arXiv URL to PDF URL
        arxiv_id = self._extract_arxiv_id(url)
        if not arxiv_id:
            raise ValueError("Could not extract arXiv ID from URL")
        
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        return self._process_pdf_url(pdf_url)
    
    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv ID from URL."""
        patterns = [
            r'arxiv\.org/abs/([^/\s]+)',
            r'arxiv\.org/pdf/([^/\s]+)',
            r'arxiv:([^/\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                arxiv_id = match.group(1)
                # Remove .pdf extension if present
                if arxiv_id.endswith('.pdf'):
                    arxiv_id = arxiv_id[:-4]
                return arxiv_id
        
        return ""
    
    def _process_pdf_url(self, url: str) -> Tuple[str, str]:
        """Download and process PDF from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            try:
                # Process the PDF
                from .pdf_processor import PDFProcessor
                processor = PDFProcessor()
                text_content = processor.extract_text(temp_path)
                title = processor.extract_title(text_content)
                
                return text_content, title
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            raise Exception(f"Error processing PDF URL: {str(e)}")
    
    def _process_web_page(self, url: str) -> Tuple[str, str]:
        """Extract text content from a web page."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Basic HTML text extraction
            html_content = response.text
            
            # Remove HTML tags (basic approach)
            text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', '', text)
            
            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r' +', ' ', text)
            
            # Extract title from HTML
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Web Page Content"
            
            # Clean title
            title = re.sub(r'<[^>]+>', '', title)
            title = title.strip()
            
            if not text.strip():
                raise ValueError("No text content could be extracted from the web page")
            
            return text.strip(), title
            
        except Exception as e:
            raise Exception(f"Error processing web page: {str(e)}")
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def get_content_type(self, url: str) -> str:
        """Get the content type of a URL."""
        try:
            response = self.session.head(url, timeout=10)
            return response.headers.get('content-type', '').lower()
        except Exception:
            return ""
