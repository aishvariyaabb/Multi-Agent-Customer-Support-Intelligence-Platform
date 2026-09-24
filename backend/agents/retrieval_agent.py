"""
Retrieval Agent: Retrieves relevant documents from knowledge base
"""
import time
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent, AgentResult
from backend.rag import RAGPipeline
from backend.config import get_settings


class RetrievalAgent(BaseAgent):
    """Retrieval agent for RAG"""
    
    def __init__(self, rag_pipeline: RAGPipeline = None):
        """Initialize retrieval agent"""
        super().__init__(
            agent_name="Retrieval Agent",
            agent_role="Knowledge Base & FAQ Retrieval"
        )
        self.settings = get_settings()
        self.rag_pipeline = rag_pipeline or self._init_pipeline()
    
    def _init_pipeline(self) -> RAGPipeline:
        """Initialize RAG pipeline"""
        return RAGPipeline(self.settings.faiss_index_path)
    
    def execute(
        self,
        ticket_text: str,
        cleaned_text: str = None,
        category: str = None,
        **kwargs
    ) -> AgentResult:
        """
        Retrieve relevant documents for ticket
        
        Args:
            ticket_text: Original ticket text
            cleaned_text: Cleaned ticket text
            category: Ticket category
        
        Returns:
            AgentResult with retrieved documents
        """
        start_time = time.time()
        
        try:
            # Use cleaned text for better retrieval
            query_text = cleaned_text if cleaned_text else ticket_text
            
            # Retrieve documents
            retrieved_docs = self.rag_pipeline.retrieve_relevant_documents(
                query=query_text,
                top_k=self.settings.rag_top_k,
                similarity_threshold=self.settings.similarity_threshold
            )
            
            # Generate response context
            context = self.rag_pipeline.generate_response_context(
                query_text,
                top_k=self.settings.rag_top_k
            )
            
            output = {
                'retrieved_documents': retrieved_docs,
                'document_count': len(retrieved_docs),
                'response_context': context,
                'top_similarity_score': retrieved_docs[0]['similarity_score'] if retrieved_docs else 0.0
            }
            
            execution_time = (time.time() - start_time) * 1000
            
            return AgentResult(
                agent_name=self.agent_name,
                status="success",
                output=output,
                execution_time_ms=execution_time
            )
        
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return AgentResult(
                agent_name=self.agent_name,
                status="error",
                output={},
                error_message=str(e),
                execution_time_ms=execution_time
            )
