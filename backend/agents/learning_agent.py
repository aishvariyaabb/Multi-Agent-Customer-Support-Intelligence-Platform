"""
Learning Agent: Analyzes outcomes and improves system
"""
import time
import json
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent, AgentResult
from sqlalchemy.orm import Session


class LearningAgent(BaseAgent):
    """Learning agent for continuous improvement"""
    
    def __init__(self):
        """Initialize learning agent"""
        super().__init__(
            agent_name="Learning Agent",
            agent_role="System Learning & Optimization"
        )
    
    def execute(
        self,
        ticket_id: str = None,
        customer_feedback: str = None,
        was_helpful: bool = None,
        satisfaction_score: int = None,
        agent_logs: list = None,
        **kwargs
    ) -> AgentResult:
        """
        Analyze outcomes and generate learning insights
        
        Args:
            ticket_id: Ticket ID
            customer_feedback: Customer feedback text
            was_helpful: Whether response was helpful
            satisfaction_score: Customer satisfaction (1-5)
            agent_logs: Logs from all agents
        
        Returns:
            AgentResult with learning insights
        """
        start_time = time.time()
        
        try:
            insights = {
                'improvement_areas': [],
                'positive_aspects': [],
                'recommendations': [],
                'system_patterns': {}
            }
            
            # Analyze if response was helpful
            if was_helpful is False:
                insights['improvement_areas'].append("Response did not resolve customer issue")
                insights['recommendations'].append("Review retrieval results and response generation")
            elif was_helpful is True:
                insights['positive_aspects'].append("Response successfully resolved issue")
            
            # Analyze satisfaction score
            if satisfaction_score:
                if satisfaction_score <= 2:
                    insights['improvement_areas'].append(f"Low satisfaction score: {satisfaction_score}/5")
                    insights['recommendations'].append("Conduct deeper analysis of customer needs")
                elif satisfaction_score >= 4:
                    insights['positive_aspects'].append(f"High satisfaction score: {satisfaction_score}/5")
            
            # Analyze feedback text
            if customer_feedback:
                feedback_insights = self._analyze_feedback(customer_feedback)
                insights['improvement_areas'].extend(feedback_insights['issues'])
                insights['positive_aspects'].extend(feedback_insights['positive'])
            
            # Analyze agent execution patterns
            if agent_logs:
                patterns = self._analyze_agent_patterns(agent_logs)
                insights['system_patterns'] = patterns
            
            output = {
                'ticket_id': ticket_id,
                'insights': insights,
                'learning_score': self._calculate_learning_score(insights),
                'ready_for_model_update': len(insights['improvement_areas']) > 0
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
    
    def _analyze_feedback(self, feedback: str) -> dict:
        """Analyze customer feedback text"""
        issues = []
        positive = []
        
        feedback_lower = feedback.lower()
        
        # Issue keywords
        issue_keywords = {
            'slow': 'Response time was slow',
            'confusing': 'Response was unclear or confusing',
            'wrong': 'Incorrect solution provided',
            'unhelpful': 'Response was not helpful',
            'rude': 'Communication tone was inappropriate'
        }
        
        # Positive keywords
        positive_keywords = {
            'quick': 'Fast response time',
            'clear': 'Clear and understandable response',
            'helpful': 'Helpful and relevant response',
            'professional': 'Professional communication'
        }
        
        for keyword, description in issue_keywords.items():
            if keyword in feedback_lower:
                issues.append(description)
        
        for keyword, description in positive_keywords.items():
            if keyword in feedback_lower:
                positive.append(description)
        
        return {'issues': issues, 'positive': positive}
    
    def _analyze_agent_patterns(self, agent_logs: list) -> dict:
        """Analyze patterns in agent execution"""
        patterns = {
            'agent_success_rates': {},
            'average_execution_times': {},
            'common_errors': []
        }
        
        if not agent_logs:
            return patterns
        
        agent_counts = {}
        agent_successes = {}
        agent_times = {}
        
        for log in agent_logs:
            agent_name = log.get('agent_name', 'Unknown')
            status = log.get('status', 'unknown')
            execution_time = log.get('execution_time_ms', 0)
            
            # Track counts
            if agent_name not in agent_counts:
                agent_counts[agent_name] = 0
                agent_successes[agent_name] = 0
                agent_times[agent_name] = []
            
            agent_counts[agent_name] += 1
            if status == 'success':
                agent_successes[agent_name] += 1
            agent_times[agent_name].append(execution_time)
        
        # Calculate success rates
        for agent_name in agent_counts:
            success_rate = agent_successes[agent_name] / agent_counts[agent_name]
            patterns['agent_success_rates'][agent_name] = success_rate
            avg_time = sum(agent_times[agent_name]) / len(agent_times[agent_name])
            patterns['average_execution_times'][agent_name] = avg_time
        
        return patterns
    
    def _calculate_learning_score(self, insights: dict) -> float:
        """Calculate learning score (0-1)"""
        score = 0.5  # Base score
        
        # Reduce for improvement areas
        score -= min(len(insights['improvement_areas']) * 0.1, 0.3)
        
        # Increase for positive aspects
        score += min(len(insights['positive_aspects']) * 0.1, 0.3)
        
        # Increase for recommendations
        score += min(len(insights['recommendations']) * 0.05, 0.2)
        
        return max(min(score, 1.0), 0.0)
