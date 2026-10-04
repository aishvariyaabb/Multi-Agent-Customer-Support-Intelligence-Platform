"""
Classification Agent: Categorizes tickets and assigns priority
"""
import time
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent, AgentResult
from backend.models import get_model_manager


class ClassificationAgent(BaseAgent):
    """Classification agent for ticket categorization"""
    
    def __init__(self):
        """Initialize classification agent"""
        super().__init__(
            agent_name="Classification Agent",
            agent_role="Ticket Categorization & Priority Assignment"
        )
        self.model_manager = get_model_manager()
    
    def execute(
        self,
        ticket_text: str,
        cleaned_text: str = None,
        sentiment: str = None,
        **kwargs
    ) -> AgentResult:
        """
        Classify ticket into category and priority
        
        Args:
            ticket_text: Original ticket text
            cleaned_text: Cleaned ticket text
            sentiment: Sentiment from intake agent
        
        Returns:
            AgentResult with classification results
        """
        start_time = time.time()
        
        try:
            # Use cleaned text if available
            text_for_classification = cleaned_text if cleaned_text else ticket_text
            
            # Predict category
            category, category_confidence = self.model_manager.category_classifier.predict(text_for_classification)
            
            # Predict priority
            priority, priority_confidence = self.model_manager.priority_classifier.predict(
                text_for_classification,
                sentiment=sentiment
            )
            
            # Extract intent
            intent_result = self.model_manager.intent_extractor.extract_intent(text_for_classification)
            
            output = {
                'category': category,
                'category_confidence': float(category_confidence),
                'priority': priority,
                'priority_confidence': float(priority_confidence),
                'intent': intent_result['primary_intent'],
                'intent_confidence': float(intent_result['confidence']),
                'all_intents': intent_result['all_intents']
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
