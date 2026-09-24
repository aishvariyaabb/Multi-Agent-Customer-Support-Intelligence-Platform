"""
Response Agent: Generates contextual responses
"""
import time
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent, AgentResult


class ResponseAgent(BaseAgent):
    """Response agent for generating ticket responses"""
    
    def __init__(self):
        """Initialize response agent"""
        super().__init__(
            agent_name="Response Agent",
            agent_role="Contextual Response Generation"
        )
    
    def execute(
        self,
        ticket_text: str,
        category: str = None,
        priority: str = None,
        sentiment: str = None,
        retrieved_context: str = None,
        customer_name: str = None,
        **kwargs
    ) -> AgentResult:
        """
        Generate response for ticket
        
        Args:
            ticket_text: Original ticket text
            category: Ticket category
            priority: Ticket priority
            sentiment: Customer sentiment
            retrieved_context: Context from RAG
            customer_name: Customer name for personalization
        
        Returns:
            AgentResult with generated response
        """
        start_time = time.time()
        
        try:
            # Generate base response template
            response = self._generate_response(
                ticket_text=ticket_text,
                category=category,
                priority=priority,
                sentiment=sentiment,
                retrieved_context=retrieved_context,
                customer_name=customer_name
            )
            
            # Calculate response quality score (0-1)
            quality_score = self._calculate_quality_score(
                response=response,
                has_context=bool(retrieved_context and len(retrieved_context) > 50),
                is_personalized=bool(customer_name)
            )
            
            output = {
                'generated_response': response,
                'quality_score': quality_score,
                'tone': self._detect_tone(sentiment),
                'response_length': len(response)
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
    
    def _generate_response(
        self,
        ticket_text: str,
        category: str = None,
        priority: str = None,
        sentiment: str = None,
        retrieved_context: str = None,
        customer_name: str = None
    ) -> str:
        """Generate response based on ticket details"""
        
        greeting = f"Hello {customer_name}," if customer_name else "Hello,"
        base_response = f"{greeting}\n\nThank you for contacting us.\n\n"
        
        # Add category-specific response
        category_responses = {
            'delivery': "We're looking into your delivery issue and will have an update for you shortly.",
            'refund': "We understand your refund request. Our team will process this promptly.",
            'payment': "Thank you for bringing the payment issue to our attention. We're investigating this.",
            'product_issue': "We're sorry to hear about the product issue. We'll help resolve this.",
            'order_tracking': "You can track your order status in real-time through your account dashboard.",
            'account': "We'll help you with your account issue right away.",
        }
        
        base_response += category_responses.get(category, "We're here to help with your issue.\n\n")
        
        # Add context from RAG if available
        if retrieved_context and len(retrieved_context) > 50:
            base_response += f"{retrieved_context}\n\n"
        
        # Add priority-specific handling note
        if priority in ['high', 'critical']:
            base_response += "This is marked as a priority issue and will receive immediate attention.\n\n"
        
        # Closing
        base_response += "If you need further assistance, please don't hesitate to reach out. We're here to help!\n\n"
        base_response += "Best regards,\nCustomer Support Team"
        
        return base_response
    
    def _detect_tone(self, sentiment: str) -> str:
        """Detect appropriate tone based on sentiment"""
        tone_map = {
            'very_negative': 'apologetic_and_reassuring',
            'negative': 'understanding_and_helpful',
            'neutral': 'professional_and_helpful',
            'positive': 'friendly_and_professional',
            'very_positive': 'warm_and_appreciative'
        }
        return tone_map.get(sentiment, 'professional_and_helpful')
    
    def _calculate_quality_score(self, response: str, has_context: bool = False, is_personalized: bool = False) -> float:
        """Calculate response quality score"""
        score = 0.6  # Base score
        
        # Bonus for length (more detailed)
        if len(response) > 200:
            score += 0.15
        
        # Bonus for context usage
        if has_context:
            score += 0.15
        
        # Bonus for personalization
        if is_personalized:
            score += 0.1
        
        return min(score, 1.0)
