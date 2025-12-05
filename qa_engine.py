"""
Question-answering engine using ChromaDB retrieval and GPT4All.
Strictly answers from document context only.
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from gpt4all import GPT4All
from typing import List, Dict, Optional


class QAEngine:
    def __init__(self, db_path: str = "./chroma_db", 
                 model_name: str = "all-MiniLM-L6-v2",
                 gpt4all_model: str = "ggml-gpt4all-j-v1.3-groovy.bin"):
        """
        Initialize QA engine with ChromaDB and GPT4All.
        
        Args:
            db_path: Path to ChromaDB data
            model_name: SentenceTransformer model name
            gpt4all_model: GPT4All model filename
        """
        self.embedding_model = SentenceTransformer(model_name)
        
        # Connect to ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory=db_path,
            anonymized_telemetry=False
        ))
        
        try:
            self.collection = self.client.get_collection("exam_documents")
        except:
            self.collection = None
        
        # Initialize GPT4All
        self.llm = None
        self.gpt4all_model = gpt4all_model
        self._load_llm()
    
    def _load_llm(self):
        """Load GPT4All model."""
        try:
            self.llm = GPT4All(self.gpt4all_model)
            print(f"GPT4All model loaded: {self.gpt4all_model}")
        except Exception as e:
            print(f"Error loading GPT4All model: {e}")
            print("Please ensure the model file is in the correct location.")
            self.llm = None
    
    def retrieve_context(self, question: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve most relevant document chunks for the question.
        
        Args:
            question: User's question
            top_k: Number of top results to retrieve
        
        Returns:
            List of relevant document chunks with metadata
        """
        if not self.collection:
            return []
        
        # Generate question embedding
        question_embedding = self.embedding_model.encode([question])[0]
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=top_k
        )
        
        # Format results
        contexts = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                contexts.append({
                    'text': doc,
                    'source': results['metadatas'][0][i].get('source', 'Unknown'),
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return contexts
    
    def generate_answer(self, question: str, contexts: List[Dict]) -> str:
        """
        Generate answer using GPT4All based strictly on retrieved context.
        
        Args:
            question: User's question
            contexts: Retrieved document contexts
        
        Returns:
            Generated answer or "Answer not found" message
        """
        if not self.llm:
            return "Error: Language model not loaded. Please check GPT4All installation."
        
        if not contexts:
            return "Answer not found in the provided exam materials."
        
        # Combine contexts
        context_text = "\n\n".join([ctx['text'] for ctx in contexts])
        
        # Create strict prompt
        prompt = f"""You are an exam assistant. Answer the question using ONLY the information provided in the context below. If the answer cannot be found in the context, respond with exactly: "Answer not found in the provided exam materials."

Context:
{context_text}

Question: {questio
n}"

Answer:"""
        
        # Generate answer with strict parameters
        try:
            response = self.llm.generate(
                prompt,
                max_tokens=300,
                temp=0.1,  # Low temperature for factual responses
                top_k=1,
                top_p=0.1
            )
            
            answer = response.strip()
            
            # Validate answer quality
            if not answer or len(answer) < 10:
                return "Answer not found in the provided exam materials."
            
            return answer
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Error generating answer. Please try again."
    
    def answer_question(self, question: str, top_k: int = 3) -> Dict:
        """
        Complete QA pipeline: retrieve context and generate answer.
        
        Args:
            question: User's question
            top_k: Number of context chunks to retrieve
        
        Returns:
            Dictionary with answer and metadata
        """
        if not question or not question.strip():
            return {
                'answer': "Please provide a valid question.",
                'contexts': [],
                'sources': []
            }
        
        # Retrieve relevant contexts
        contexts = self.retrieve_context(question, top_k)
        
        if not contexts:
            return {
                'answer': "Answer not found in the provided exam materials.",
                'contexts': [],
                'sources': []
            }
        
        # Generate answer
        answer = self.generate_answer(question, contexts)
        
        # Extract unique sources
        sources = list(set([ctx['source'] for ctx in contexts]))
        
        return {
            'answer': answer,
            'contexts': contexts,
            'sources': sources
        }
