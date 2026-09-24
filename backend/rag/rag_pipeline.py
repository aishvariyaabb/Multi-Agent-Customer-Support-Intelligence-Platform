"""
RAG (Retrieval Augmented Generation) Pipeline with FAISS
"""
import os
import pickle
import numpy as np
import faiss
from typing import List, Tuple, Dict, Any
from backend.utils import get_embedder


class FAISSVectorStore:
    """FAISS vector database for similarity search"""
    
    def __init__(self, index_path: str, embedding_dim: int = 384):
        """Initialize FAISS vector store"""
        self.index_path = index_path
        self.embedding_dim = embedding_dim
        self.index = None
        self.documents = []  # Store document texts
        self.metadata = []   # Store document metadata
        
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create a new one"""
        if os.path.exists(self.index_path):
            with open(self.index_path, 'rb') as f:
                data = pickle.load(f)
                self.index = data['index']
                self.documents = data['documents']
                self.metadata = data['metadata']
        else:
            # Create new FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_dim)
    
    def add_documents(self, documents: List[str], metadata_list: List[Dict[str, Any]] = None):
        """Add documents to the vector store"""
        embedder = get_embedder()
        
        # Generate embeddings
        embeddings = embedder.encode_texts(documents)
        embeddings = embeddings.astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store documents and metadata
        self.documents.extend(documents)
        if metadata_list is None:
            metadata_list = [{'id': i} for i in range(len(documents))]
        self.metadata.extend(metadata_list)
        
        self.save()
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict, float]]:
        """Search for similar documents"""
        if self.index.ntotal == 0:
            return []
        
        embedder = get_embedder()
        query_embedding = embedder.encode_text(query).astype('float32')
        query_embedding = query_embedding.reshape(1, -1)
        
        # Search in FAISS
        distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            # Convert L2 distance to similarity score (0-1)
            # Smaller distance = higher similarity
            similarity = 1 / (1 + distance)
            
            if idx < len(self.documents):
                results.append((
                    self.documents[idx],
                    self.metadata[idx],
                    float(similarity)
                ))
        
        return results
    
    def save(self):
        """Save index to disk"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, 'wb') as f:
            pickle.dump({
                'index': self.index,
                'documents': self.documents,
                'metadata': self.metadata
            }, f)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            'total_documents': self.index.ntotal,
            'embedding_dimension': self.embedding_dim,
            'index_size_mb': os.path.getsize(self.index_path) / (1024 * 1024) if os.path.exists(self.index_path) else 0
        }


class RAGPipeline:
    """RAG pipeline for ticket resolution"""
    
    def __init__(self, vector_store_path: str):
        """Initialize RAG pipeline"""
        self.vector_store = FAISSVectorStore(vector_store_path)
    
    def add_faq_documents(self, faqs: List[Dict[str, str]]):
        """Add FAQ documents to the vector store"""
        texts = []
        metadata = []
        
        for idx, faq in enumerate(faqs):
            text = f"{faq.get('question', '')} {faq.get('answer', '')}"
            texts.append(text)
            metadata.append({
                'id': f"faq_{idx}",
                'type': 'faq',
                'question': faq.get('question', ''),
                'answer': faq.get('answer', ''),
                'category': faq.get('category', '')
            })
        
        self.vector_store.add_documents(texts, metadata)
    
    def add_past_tickets(self, tickets: List[Dict[str, str]]):
        """Add past resolved tickets to the vector store"""
        texts = []
        metadata = []
        
        for idx, ticket in enumerate(tickets):
            text = f"{ticket.get('title', '')} {ticket.get('description', '')} {ticket.get('resolution', '')}"
            texts.append(text)
            metadata.append({
                'id': f"ticket_{idx}",
                'type': 'past_ticket',
                'title': ticket.get('title', ''),
                'description': ticket.get('description', ''),
                'resolution': ticket.get('resolution', ''),
                'category': ticket.get('category', '')
            })
        
        self.vector_store.add_documents(texts, metadata)
    
    def retrieve_relevant_documents(
        self, 
        query: str, 
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        raw_results = self.vector_store.search(query, top_k=top_k)
        
        results = []
        for text, metadata, similarity in raw_results:
            if similarity >= similarity_threshold:
                results.append({
                    'type': metadata.get('type', 'unknown'),
                    'content': text,
                    'similarity_score': similarity,
                    'metadata': metadata
                })
        
        return results
    
    def generate_response_context(self, query: str, top_k: int = 3) -> str:
        """Generate context for response generation"""
        documents = self.retrieve_relevant_documents(query, top_k=top_k)
        
        if not documents:
            return "No relevant documents found in knowledge base."
        
        context = "Based on our knowledge base:\n\n"
        for doc in documents:
            if doc['type'] == 'faq':
                context += f"Q: {doc['metadata'].get('question', '')}\n"
                context += f"A: {doc['metadata'].get('answer', '')}\n\n"
            elif doc['type'] == 'past_ticket':
                context += f"Similar Issue: {doc['metadata'].get('title', '')}\n"
                context += f"Resolution: {doc['metadata'].get('resolution', '')}\n\n"
        
        return context
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG pipeline statistics"""
        return self.vector_store.get_stats()
