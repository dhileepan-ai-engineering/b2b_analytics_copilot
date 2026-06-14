import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from src.agents import AgenticWorkflowEngine
from src.glossary import SemanticGlossaryPipeline

app = FastAPI(
    title="Assistant - GenAI Pipeline API",
    version="1.0.0",
    description="Microservice for multi-agent orchestration, analytics synthesis, compliance verification, and data tutoring."
)

class QueryRequest(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "Analyze our current MDF allocation..."})

class QueryResponse(BaseModel):
    intent: str
    executive_summary: str
    telemetry: dict

@app.post("/v1/execute", response_model=QueryResponse, tags=["Agentic Workflow"])
async def execute_workflow(payload: QueryRequest):
    """
    Enterprise sandbox endpoint to route queries, expand glossary terms, 
    execute targeted LLM generation agents, and enforce compliance audits.
    """
    try:
        # 1. Glossary expansion
        # Note: If your method in glossary.py is named expand_query_context, leave it as is.
        # If it was updated during path refactoring, verify it matches here.
        glossary_pipe = SemanticGlossaryPipeline()
        expanded_prompt = glossary_pipe.expand_query_context(payload.query)
        
        # 2. Initialize Agent Workflow Engine and Route Intent
        engine = AgenticWorkflowEngine()
        intent, router_audit = await engine.route_intent(expanded_prompt)
        
        # Initialize telemetry block container
        telemetry_data = {
            "router": router_audit
        }
        
        # 3. Conditional Execution Pathway
        if "STRATEGIC_ANALYTICS" in intent:
            # Generate initial business insights report
            draft_report, agent_audit = await engine.execute_analytics(expanded_prompt)
            telemetry_data["execution_node"] = agent_audit
            
            # 4. Closed-loop Compliance Audit Step
            audit_verdict, compliance_audit = await engine.verify_financial_compliance(
                analysis_report=draft_report,
                baseline_query=payload.query
            )
            telemetry_data["compliance_node"] = compliance_audit
            
            # Combine the insights and audit verification stamp into the final asset
            final_output = f"{draft_report}\n\n[Compliance Audit Review]: {audit_verdict}"
            
        else:
            # Route to Data Tutor node for terminology onboarding
            final_output, agent_audit = await engine.execute_data_tutor(expanded_prompt)
            telemetry_data["execution_node"] = agent_audit

        return QueryResponse(
            intent=intent,
            executive_summary=final_output,
            telemetry=telemetry_data
        )
        
    except Exception as e:
        # Proper enterprise error masking and tracking
        raise HTTPException(status_code=500, detail=f"Internal Agentic Pipeline Failure: {str(e)}")

@app.get("/health", tags=["Infrastructure"])
def health_check():
    """Liveness/Readiness probe for container orchestration/deployment platforms."""
    return {"status": "healthy", "pipeline_active": True}