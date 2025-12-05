"""
Document loading, embedding generation, and ChromaDB storage module.
Handles PDF, DOCX, and TXT files for offline exam system.
"""

import os
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import hashlib


class DocumentStore:
    def __init__(self, db_path: str = "./chroma_db", model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize document store with local ChromaDB and SentenceTransformer.
        
        Args:
            db_path: Path to store ChromaDB data
            model_name: SentenceTransformer model name
        """
        self.db_path = db_path
        self.embedding_model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB with local persistence
        self.client = chromadb.Client(Settings(
            persist_directory=db_path,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="exam_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text.strip()
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
        return text.strip()
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file type: {ext}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval.
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum characters per chunk
            overlap: Overlapping characters between chunks
        
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]
    
    def load_documents(self, file_paths: List[str]) -> Dict[str, int]:
        """
        Load multiple documents, extract text, generate embeddings, and store in ChromaDB.
        
        Args:
            file_paths: List of document file paths
        
        Returns:
            Dictionary with statistics
        """
        total_chunks = 0
        processed_files = 0
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
            
            print(f"Processing: {file_path}")
            
            # Extract text
            text = self.extract_text(file_path)
            if not text:
                print(f"No text extracted from: {file_path}")
                continue
            
            # Chunk text
            chunks = self.chunk_text(text)
            if not chunks:
                continue
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
            
            # Create unique IDs for chunks
            file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
            ids = [f"{file_hash}_{i}" for i in range(len(chunks))]
            
            # Store in ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=chunks,
                ids=ids,
                metadatas=[{"source": os.path.basename(file_path)} for _ in chunks]
            )
            
            total_chunks += len(chunks)
            processed_files += 1
            print(f"  Added {len(chunks)} chunks")
        
        return {
            "processed_files": processed_files,
            "total_chunks": total_chunks
        }
    
    def clear_database(self):
        """Clear all documents from the database."""
        try:
            self.client.delete_collection("exam_documents")
            self.collection = self.client.get_or_create_collection(
                name="exam_documents",
                metadata={"hnsw:space": "cosine"}
            )
            print("Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {e}")
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
