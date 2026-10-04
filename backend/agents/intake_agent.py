"""
Intake Agent: Cleans text and extracts key information
"""
import time
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent, AgentResult
from backend.utils import TextProcessor, SentimentAnalyzer


class IntakeAgent(BaseAgent):
    """Intake agent for ticket preprocessing"""
    
    def __init__(self):
        """Initialize intake agent"""
        super().__init__(
            agent_name="Intake Agent",
            agent_role="Text Processing & Entity Extraction"
        )
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def execute(self, ticket_text: str, customer_name: str = None, customer_email: str = None) -> AgentResult:
        """
        Process incoming ticket
        
        Args:
            ticket_text: Raw ticket text
            customer_name: Customer name
            customer_email: Customer email
        
        Returns:
            AgentResult with processed data
        """
        start_time = time.time()
        
        try:
            # Clean text
            cleaned_text = self.text_processor.clean_text(ticket_text)
            
            # Extract entities
            entities = self.text_processor.extract_entities(ticket_text)
            
            # Analyze sentiment
            sentiment, sentiment_confidence = self.sentiment_analyzer.analyze_sentiment(ticket_text)
            
            # Get text statistics
            stats = self.text_processor.get_text_length_stats(cleaned_text)
            
            # Extract sentiment keywords
            sentiment_keywords = self.sentiment_analyzer.get_sentiment_keywords(ticket_text)
            
            output = {
                'original_text': ticket_text,
                'cleaned_text': cleaned_text,
                'entities': entities,
                'sentiment': sentiment,
                'sentiment_confidence': float(sentiment_confidence),
                'sentiment_keywords': sentiment_keywords,
                'text_statistics': stats,
                'customer_name': customer_name,
                'customer_email': customer_email
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
