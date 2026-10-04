"""
Response Agent: Generates contextual responses
"""
import os
import time
from typing import Dict, Any

from backend.agents.base_agent import BaseAgent, AgentResult
from backend.config import get_settings

try:
    from crewai import Agent as CrewAIAgent
    from crewai import Crew
    from crewai import Task as CrewAITask
    from crewai import LLM
except Exception:  # pragma: no cover - optional dependency
    CrewAIAgent = None
    Crew = None
    CrewAITask = None
    LLM = None


class ResponseAgent(BaseAgent):
    """Response agent for generating ticket responses"""

    def __init__(self):
        """Initialize response agent"""
        super().__init__(
            agent_name="Response Agent",
            agent_role="Contextual Response Generation"
        )
        self.settings = get_settings()
        self.api_key = os.getenv("OPENAI_API_KEY") or self.settings.openai_api_key
        self.base_url = os.getenv("OPENAI_BASE_URL") or self.settings.openai_base_url
        self.model_name = os.getenv("OPENAI_MODEL") or self.settings.openai_model
        self._validate_llm_configuration()
        self.llm = self._build_llm()

    def _validate_llm_configuration(self):
        """Reject placeholder or empty API keys so the app cannot run without a real Gemini key."""
        invalid_markers = {
            "",
            "abcd",
            "test",
            "demo",
            "example",
            "placeholder",
            "your_api_key_here",
            "your-gemini-api-key",
            "ollama",
            "openai",
        }

        key = (self.api_key or "").strip()
        if not key or key.lower() in invalid_markers:
            raise RuntimeError(
                "Gemini API key is required. Set OPENAI_API_KEY to a valid Gemini key in .env. "
                "Without a valid API key, the app must fail instead of returning fallback output."
            )

        if not self.base_url:
            raise RuntimeError(
                "Gemini base URL is required. Set OPENAI_BASE_URL to the Gemini OpenAI-compatible endpoint."
            )

        if not self.model_name:
            raise RuntimeError("Gemini model name is required. Set OPENAI_MODEL to a valid Gemini model like gemini-3.8-flash.")

    def _build_llm(self):
        """Build CrewAI LLM instance using the configured Gemini/OpenAI-compatible endpoint."""
        if LLM is None:
            raise RuntimeError("CrewAI LLM dependency is not available.")

        try:
            llm_kwargs = {
                "model": self.model_name,
                "temperature": 0.2,
                "api_key": self.api_key,
                "base_url": self.base_url,
            }
            return LLM(**llm_kwargs)
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Gemini LLM client: {exc}") from exc

    def _generate_llm_response(
        self,
        ticket_text: str,
        category: str = None,
        priority: str = None,
        sentiment: str = None,
        retrieved_context: str = None,
        customer_name: str = None
    ) -> str:
        """Generate a support reply using the Gemini API via CrewAI LLM client without synchronous Crew kickoff."""
        if self.llm is None:
            raise RuntimeError("LLM client is unavailable. The system requires a valid Gemini API key and API-backed model response.")

        customer_context = f"Customer name: {customer_name}" if customer_name else "Customer name: unknown"
        context_block = retrieved_context or "No additional knowledge base context provided."
        prompt = (
            "You are a helpful and empathetic customer support agent. "
            f"Respond to the following customer ticket.\n\n"
            f"Customer: {customer_context}\n"
            f"Category: {category or 'general'}\n"
            f"Priority: {priority or 'medium'}\n"
            f"Sentiment: {sentiment or 'neutral'}\n"
            f"Knowledge context: {context_block}\n\n"
            f"Ticket:\n{ticket_text}\n\n"
            "Write a concise but professional support reply. "
            "Acknowledge the issue, show empathy, provide a clear next step, and keep it customer-friendly."
        )

        answer = str(self.llm.call(prompt)).strip()
        if answer:
            return answer

        raise RuntimeError("Gemini returned an empty response. A valid API-backed response is required.")

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
        Generate response for ticket using the API-backed LLM only.
        """
        start_time = time.time()

        try:
            response = self._generate_llm_response(
                ticket_text=ticket_text,
                category=category,
                priority=priority,
                sentiment=sentiment,
                retrieved_context=retrieved_context,
                customer_name=customer_name,
            )

            quality_score = self._calculate_quality_score(
                response=response,
                has_context=bool(retrieved_context and len(retrieved_context) > 50),
                is_personalized=bool(customer_name)
            )

            output = {
                'generated_response': response,
                'quality_score': quality_score,
                'tone': self._detect_tone(sentiment),
                'response_length': len(response),
                'llm_used': True
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
        """This fallback is intentionally disabled. The app must use the API-backed Gemini model only."""
        raise RuntimeError(
            "No fallback response is allowed. Please provide a valid Gemini API key and ensure the API-backed LLM is available."
        )

    def _calculate_quality_score(self, response: str, has_context: bool = False, is_personalized: bool = False) -> float:
        """Return a lightweight quality score for the generated response."""
        score = 0.5
        if response and len(response.strip()) > 40:
            score += 0.25
        if has_context:
            score += 0.15
        if is_personalized:
            score += 0.10
        return round(min(score, 1.0), 2)

    def _detect_tone(self, sentiment: str = None) -> str:
        """Infer a tone label from the ticket sentiment."""
        sentiment_value = (sentiment or '').lower()
        if sentiment_value in {'very_negative', 'negative'}:
            return 'empathetic'
        if sentiment_value in {'positive', 'very_positive'}:
            return 'professional_and_helpful'
        return 'professional_and_helpful'
