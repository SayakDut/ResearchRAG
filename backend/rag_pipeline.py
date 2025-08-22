import faiss
import numpy as np
from typing import List, Dict
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import pickle
from pathlib import Path

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        
        self.dimension = 384  # Using a smaller dimension for free embeddings
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = {}
        self.chunks = {}
        self.chunk_embeddings = {}
        
        # Create storage directory
        self.storage_dir = Path("rag_storage")
        self.storage_dir.mkdir(exist_ok=True)
        
        # Load existing data if available
        self._load_index()
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > start + chunk_size // 2:
                    chunk = text[start:break_point + 1]
                    end = break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(text):
                break
                
        return chunks
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text using a simple hash-based approach for free usage."""
        # For production, you'd use a proper embedding model
        # This is a simplified approach for the free tier
        import hashlib
        
        # Create a simple hash-based embedding
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to float array and normalize
        embedding = np.frombuffer(hash_bytes[:self.dimension * 4], dtype=np.float32)
        if len(embedding) < self.dimension:
            # Pad with zeros if needed
            padding = np.zeros(self.dimension - len(embedding), dtype=np.float32)
            embedding = np.concatenate([embedding, padding])
        else:
            embedding = embedding[:self.dimension]
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding
    
    def add_document(self, paper_id: str, text: str):
        """Add a document to the RAG pipeline."""
        # Chunk the document
        chunks = self._chunk_text(text)
        
        # Store document and chunks
        self.documents[paper_id] = text
        self.chunks[paper_id] = chunks
        
        # Generate embeddings for chunks
        embeddings = []
        for chunk in chunks:
            embedding = self._get_embedding(chunk)
            embeddings.append(embedding)
        
        embeddings = np.array(embeddings).astype('float32')
        self.chunk_embeddings[paper_id] = embeddings
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Save the updated index
        self._save_index()
    
    def _save_index(self):
        """Save the FAISS index and metadata."""
        # Save FAISS index
        faiss.write_index(self.index, str(self.storage_dir / "faiss.index"))
        
        # Save metadata
        metadata = {
            "documents": self.documents,
            "chunks": self.chunks,
            "chunk_embeddings": {k: v.tolist() for k, v in self.chunk_embeddings.items()}
        }
        
        with open(self.storage_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
    
    def _load_index(self):
        """Load the FAISS index and metadata."""
        index_path = self.storage_dir / "faiss.index"
        metadata_path = self.storage_dir / "metadata.json"
        
        if index_path.exists() and metadata_path.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(index_path))
                
                # Load metadata
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                self.documents = metadata.get("documents", {})
                self.chunks = metadata.get("chunks", {})
                self.chunk_embeddings = {
                    k: np.array(v, dtype='float32') 
                    for k, v in metadata.get("chunk_embeddings", {}).items()
                }
            except Exception as e:
                print(f"Error loading index: {e}")
                # Reset if loading fails
                self.index = faiss.IndexFlatL2(self.dimension)
                self.documents = {}
                self.chunks = {}
                self.chunk_embeddings = {}
    
    def _find_relevant_chunks(self, paper_id: str, query: str, top_k: int = 3) -> List[str]:
        """Find the most relevant chunks for a query."""
        if paper_id not in self.chunks:
            return []
        
        query_embedding = self._get_embedding(query).reshape(1, -1)
        
        # Get embeddings for this paper's chunks
        paper_embeddings = self.chunk_embeddings[paper_id]
        
        # Create a temporary index for this paper
        temp_index = faiss.IndexFlatL2(self.dimension)
        temp_index.add(paper_embeddings)
        
        # Search for similar chunks
        distances, indices = temp_index.search(query_embedding, min(top_k, len(self.chunks[paper_id])))
        
        # Return the relevant chunks
        relevant_chunks = []
        for idx in indices[0]:
            if idx < len(self.chunks[paper_id]):
                relevant_chunks.append(self.chunks[paper_id][idx])
        
        return relevant_chunks
    
    def query(self, paper_id: str, query: str) -> str:
        """Query the RAG pipeline for a specific paper."""
        if paper_id not in self.documents:
            return "Paper not found in the system."
        
        # Find relevant chunks
        relevant_chunks = self._find_relevant_chunks(paper_id, query)
        
        if not relevant_chunks:
            return "No relevant information found for your query."
        
        # Prepare context
        context = "\n\n".join(relevant_chunks)
        
        # Create prompt
        prompt = f"""Based on the following context from a research paper, please answer the question.

Context:
{context}

Question: {query}

Please provide a comprehensive answer based only on the information provided in the context. If the context doesn't contain enough information to answer the question, please say so."""

        try:
            # Get response from LLM
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "ResearchRAG",
                }
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
