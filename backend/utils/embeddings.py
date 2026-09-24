"""
Embedding and similarity utilities
"""
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingManager:
    """Manage text embeddings"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedder with a pre-trained model"""
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode a single text to embedding"""
        return self.model.encode(text, convert_to_numpy=True)
    
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts to embeddings"""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute similarity between two texts"""
        emb1 = self.encode_text(text1).reshape(1, -1)
        emb2 = self.encode_text(text2).reshape(1, -1)
        similarity = cosine_similarity(emb1, emb2)[0][0]
        return float(similarity)
    
    def compute_similarities(self, query: str, documents: List[str]) -> List[Tuple[str, float]]:
        """Compute similarities between query and multiple documents"""
        query_emb = self.encode_text(query).reshape(1, -1)
        doc_embs = self.encode_texts(documents)
        
        similarities = cosine_similarity(query_emb, doc_embs)[0]
        results = [(doc, sim) for doc, sim in zip(documents, similarities)]
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def get_embedding_dimension(self) -> int:
        """Get embedding dimension"""
        return self.embedding_dim


# Global embedder instance
_embedder_instance = None


def get_embedder(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingManager:
    """Get global embedder instance (lazy loading)"""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = EmbeddingManager(model_name)
    return _embedder_instance
