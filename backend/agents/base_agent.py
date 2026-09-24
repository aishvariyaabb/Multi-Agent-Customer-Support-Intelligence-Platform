"""
Base Agent class and common agent utilities
"""
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class AgentResult:
    """Result object for agent execution"""
    agent_name: str
    status: str  # 'success', 'error', 'skipped'
    output: Dict[str, Any]
    error_message: str = None
    execution_time_ms: float = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_name: str, agent_role: str):
        """Initialize agent"""
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.agent_id = str(uuid.uuid4())
    
    def execute(self, **kwargs) -> AgentResult:
        """Execute agent task - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def log_execution(self, result: AgentResult) -> Dict[str, Any]:
        """Format agent execution for logging"""
        return {
            'agent_name': self.agent_name,
            'agent_id': self.agent_id,
            'agent_role': self.agent_role,
            'status': result.status,
            'execution_time_ms': result.execution_time_ms,
            'timestamp': result.timestamp.isoformat() if result.timestamp else None,
            'output': result.output,
            'error': result.error_message
        }
