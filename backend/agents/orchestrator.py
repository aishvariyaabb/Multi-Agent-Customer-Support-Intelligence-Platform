"""
Agent Orchestrator: Coordinates all agents in the workflow
"""
import time
from typing import Dict, Any, List
from datetime import datetime
from backend.agents import (
    IntakeAgent, ClassificationAgent, RetrievalAgent,
    ResponseAgent, EscalationAgent, LearningAgent, AgentResult
)
from backend.rag import RAGPipeline
from backend.config import get_settings
from loguru import logger


class AgentOrchestrator:
    """Orchestrates multi-agent workflow"""
    
    def __init__(self, rag_pipeline: RAGPipeline = None):
        """Initialize orchestrator with all agents"""
        self.settings = get_settings()
        
        # Initialize agents
        self.intake_agent = IntakeAgent()
        self.classification_agent = ClassificationAgent()
        self.retrieval_agent = RetrievalAgent(rag_pipeline)
        self.response_agent = ResponseAgent()
        self.escalation_agent = EscalationAgent()
        self.learning_agent = LearningAgent()
        
        self.workflow_logs = []
    
    def process_ticket(
        self,
        ticket_text: str,
        customer_name: str = None,
        customer_email: str = None,
        enable_escalation: bool = None,
        enable_rag: bool = None
    ) -> Dict[str, Any]:
        """
        Process a ticket through the entire multi-agent pipeline
        
        Args:
            ticket_text: The customer's ticket text
            customer_name: Customer name
            customer_email: Customer email
            enable_escalation: Whether to run escalation agent
            enable_rag: Whether to use RAG for retrieval
        
        Returns:
            Dictionary with complete processing results
        """
        if enable_escalation is None:
            enable_escalation = self.settings.escalation_enabled
        if enable_rag is None:
            enable_rag = self.settings.rag_enabled
        
        start_time = time.time()
        workflow_results = {
            'ticket_text': ticket_text,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'timestamp': datetime.utcnow().isoformat(),
            'agent_results': {},
            'final_response': None,
            'requires_escalation': False,
            'assigned_team': 'Customer Support',
            'total_execution_time_ms': 0
        }
        
        try:
            # Step 1: Intake Agent
            logger.info("Starting intake agent...")
            intake_result = self.intake_agent.execute(
                ticket_text=ticket_text,
                customer_name=customer_name,
                customer_email=customer_email
            )
            workflow_results['agent_results']['intake'] = intake_result.to_dict()
            
            if intake_result.status != 'success':
                raise Exception(f"Intake agent failed: {intake_result.error_message}")
            
            intake_output = intake_result.output
            
            # Step 2: Classification Agent
            logger.info("Starting classification agent...")
            classification_result = self.classification_agent.execute(
                ticket_text=ticket_text,
                cleaned_text=intake_output.get('cleaned_text'),
                sentiment=intake_output.get('sentiment')
            )
            workflow_results['agent_results']['classification'] = classification_result.to_dict()
            
            if classification_result.status != 'success':
                raise Exception(f"Classification agent failed: {classification_result.error_message}")
            
            classification_output = classification_result.output
            
            # Step 3: Retrieval Agent (with RAG)
            retrieved_context = None
            retrieved_docs_count = 0
            
            if enable_rag:
                logger.info("Starting retrieval agent...")
                retrieval_result = self.retrieval_agent.execute(
                    ticket_text=ticket_text,
                    cleaned_text=intake_output.get('cleaned_text'),
                    category=classification_output.get('category')
                )
                workflow_results['agent_results']['retrieval'] = retrieval_result.to_dict()
                
                if retrieval_result.status == 'success':
                    retrieval_output = retrieval_result.output
                    retrieved_context = retrieval_output.get('response_context')
                    retrieved_docs_count = retrieval_output.get('document_count', 0)
            
            # Step 4: Response Agent
            logger.info("Starting response agent...")
            response_result = self.response_agent.execute(
                ticket_text=ticket_text,
                category=classification_output.get('category'),
                priority=classification_output.get('priority'),
                sentiment=intake_output.get('sentiment'),
                retrieved_context=retrieved_context,
                customer_name=customer_name
            )
            workflow_results['agent_results']['response'] = response_result.to_dict()
            
            if response_result.status != 'success':
                raise Exception(f"Response agent failed: {response_result.error_message}")
            
            response_output = response_result.output
            workflow_results['final_response'] = response_output.get('generated_response')
            
            # Step 5: Escalation Agent
            if enable_escalation:
                logger.info("Starting escalation agent...")
                escalation_result = self.escalation_agent.execute(
                    category=classification_output.get('category'),
                    priority=classification_output.get('priority'),
                    sentiment=intake_output.get('sentiment'),
                    category_confidence=classification_output.get('category_confidence'),
                    response_quality_score=response_output.get('quality_score'),
                    retrieved_docs_count=retrieved_docs_count
                )
                workflow_results['agent_results']['escalation'] = escalation_result.to_dict()
                
                if escalation_result.status == 'success':
                    escalation_output = escalation_result.output
                    workflow_results['requires_escalation'] = escalation_output.get('should_escalate', False)
                    workflow_results['assigned_team'] = escalation_output.get('assigned_team', 'Customer Support')
                    workflow_results['escalation_level'] = escalation_output.get('escalation_level', 'LOW')
            
            # Step 6: Learning Agent
            logger.info("Starting learning agent...")
            learning_result = self.learning_agent.execute(
                agent_logs=[workflow_results['agent_results'].get(agent) for agent in ['intake', 'classification', 'retrieval', 'response', 'escalation']]
            )
            workflow_results['agent_results']['learning'] = learning_result.to_dict()
            
            # Compile final results
            workflow_results.update({
                'category': classification_output.get('category'),
                'priority': classification_output.get('priority'),
                'sentiment': intake_output.get('sentiment'),
                'intent': classification_output.get('intent'),
                'classification_confidence': classification_output.get('category_confidence'),
                'response_quality': response_output.get('quality_score'),
                'total_execution_time_ms': (time.time() - start_time) * 1000,
                'status': 'completed'
            })
            
            logger.info(f"Ticket processing completed in {workflow_results['total_execution_time_ms']:.2f}ms")
            
        except Exception as e:
            logger.error(f"Error in ticket processing: {str(e)}", exc_info=True)
            workflow_results['status'] = 'error'
            workflow_results['error'] = str(e)
            workflow_results['total_execution_time_ms'] = (time.time() - start_time) * 1000
        
        return workflow_results
    
    def get_workflow_summary(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of workflow execution"""
        return {
            'status': workflow_results.get('status'),
            'category': workflow_results.get('category'),
            'priority': workflow_results.get('priority'),
            'sentiment': workflow_results.get('sentiment'),
            'requires_escalation': workflow_results.get('requires_escalation'),
            'assigned_team': workflow_results.get('assigned_team'),
            'total_execution_time_ms': workflow_results.get('total_execution_time_ms'),
            'response_length': len(workflow_results.get('final_response', '')) if workflow_results.get('final_response') else 0
        }
