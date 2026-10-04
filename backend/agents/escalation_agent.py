"""
Escalation Agent: Decides whether ticket needs escalation
"""
import time
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent, AgentResult


class EscalationAgent(BaseAgent):
    """Escalation agent for routing complex tickets"""
    
    def __init__(self):
        """Initialize escalation agent"""
        super().__init__(
            agent_name="Escalation Agent",
            agent_role="Ticket Escalation & Routing"
        )
    
    def execute(
        self,
        category: str = None,
        priority: str = None,
        sentiment: str = None,
        category_confidence: float = None,
        response_quality_score: float = None,
        retrieved_docs_count: int = 0,
        **kwargs
    ) -> AgentResult:
        """
        Decide if ticket should be escalated
        
        Args:
            category: Ticket category
            priority: Ticket priority
            sentiment: Customer sentiment
            category_confidence: Classification confidence
            response_quality_score: Generated response quality
            retrieved_docs_count: Number of relevant docs found
        
        Returns:
            AgentResult with escalation decision
        """
        start_time = time.time()
        
        try:
            # Escalation logic
            should_escalate = False
            escalation_reasons = []
            escalation_score = 0.0
            
            # Check sentiment
            if sentiment in ['very_negative', 'negative']:
                should_escalate = True
                escalation_reasons.append("Customer sentiment is negative")
                escalation_score += 0.4
            
            # Check priority
            if priority in ['high', 'critical']:
                should_escalate = True
                escalation_reasons.append(f"Ticket priority is {priority}")
                escalation_score += 0.3
            
            # Check classification confidence (low confidence = escalate)
            if category_confidence and category_confidence < 0.5:
                should_escalate = True
                escalation_reasons.append("Low classification confidence")
                escalation_score += 0.2
            
            # Check if no relevant documents found (can't auto-resolve)
            if retrieved_docs_count == 0:
                escalation_score += 0.15
            
            # Check response quality
            if response_quality_score and response_quality_score < 0.5:
                should_escalate = True
                escalation_reasons.append("Generated response quality is low")
                escalation_score += 0.2
            
            # Determine assigned team
            team_assignment = self._assign_team(category, priority)
            
            # Cap escalation score at 1.0
            escalation_score = min(escalation_score, 1.0)
            
            output = {
                'should_escalate': should_escalate,
                'escalation_score': float(escalation_score),
                'escalation_reasons': escalation_reasons,
                'assigned_team': team_assignment,
                'escalation_level': self._determine_escalation_level(escalation_score, priority),
                'recommended_action': self._get_recommended_action(should_escalate, escalation_score)
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
    
    def _assign_team(self, category: str, priority: str) -> str:
        """Assign ticket to appropriate team"""
        team_map = {
            'delivery': 'Logistics Team',
            'refund': 'Finance Team',
            'payment': 'Payment Processing Team',
            'product_issue': 'Product Support Team',
            'order_tracking': 'Customer Service Team',
            'account': 'Account Management Team'
        }
        
        team = team_map.get(category, 'General Support Team')
        
        # Escalate to senior team for high priority
        if priority in ['high', 'critical']:
            team = f"Senior {team}"
        
        return team
    
    def _determine_escalation_level(self, escalation_score: float, priority: str = None) -> str:
        """Determine escalation level"""
        if priority == 'critical' or escalation_score >= 0.8:
            return 'CRITICAL'
        elif priority == 'high' or escalation_score >= 0.6:
            return 'HIGH'
        elif escalation_score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_recommended_action(self, should_escalate: bool, escalation_score: float) -> str:
        """Get recommended action"""
        if not should_escalate:
            return 'Send auto-generated response and monitor for feedback'
        elif escalation_score >= 0.8:
            return 'Immediately escalate to manager'
        elif escalation_score >= 0.6:
            return 'Route to specialized team and prioritize'
        else:
            return 'Queue for human review within SLA'
