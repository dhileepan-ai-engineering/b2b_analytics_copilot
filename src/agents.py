import os
import asyncio
from openai import AsyncOpenAI
from src.telemetry import track_ml_metrics

# Initialize client using Groq's fully compatible OpenAI routing specification
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

# Selecting high-performance open models available on the free tier
ROUTER_MODEL = "llama-3.3-70b-versatile"
ANALYTICS_MODEL = "llama-3.1-8b-instant"

class AgenticWorkflowEngine:
    
    @track_ml_metrics(node_name="Intent_Router_Node")
    async def route_intent(self, prompt: str):
        """Classifies incoming enterprise requests into deterministic processing pipelines."""
        system_instructions = (
            "You are an automated Intent Router. Categorize the user's input request into exactly "
            "one of two categories based on intent:\n"
            "1. 'STRATEGIC_ANALYTICS': If the query requires computational synthesis or business logic reasoning.\n"
            "2. 'DATA_TUTOR': If the query requests basic definitions, structural onboarding, or terminology clarification.\n"
            "Return only the raw classification string as single text token output: either STRATEGIC_ANALYTICS or DATA_TUTOR."
        )
        
        response = await client.chat.completions.create(
            model=ROUTER_MODEL,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        intent = response.choices[0].message.content.strip()
        token_meta = {
            "model": response.model,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return intent, token_meta

    @track_ml_metrics(node_name="Analytics_Execution_Node")
    async def execute_analytics(self, prompt: str):
        """Synthesizes high-dimensional B2B telemetry into automated insights."""
        system_instructions = (
            "You are the Analytics Expert agent. Process the query using provided domain glossary context. "
            "Formulate an executive response summarizing structural steps to optimize financial performance indicators."
        )
        response = await client.chat.completions.create(
            model=ANALYTICS_MODEL,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        token_meta = {
            "model": response.model,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return response.choices[0].message.content.strip(), token_meta

    @track_ml_metrics(node_name="Data_Tutor_Execution_Node")
    async def execute_data_tutor(self, prompt: str):
        """Provides foundational technical onboarding and systems glossary tracking."""
        system_instructions = (
            "You are the Data Tutor agent. Break down the enterprise system architecture or business terms "
            "clearly for a technical onboarding sandbox client."
        )
        response = await client.chat.completions.create(
            model=ANALYTICS_MODEL,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        token_meta = {
            "model": response.model,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return response.choices[0].message.content.strip(), token_meta