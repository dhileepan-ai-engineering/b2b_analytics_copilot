import asyncio
from src.glossary import SemanticGlossaryPipeline
from src.agents import AgenticWorkflowEngine

async def run_copilot_pipeline(user_query: str):
    print(f"\n[1/4] Initializing Raw Query: '{user_query}'")
    
    # Step 1: Pre-execution semantic glossary expansion
    glossary_pipe = SemanticGlossaryPipeline()
    expanded_prompt = glossary_pipe.expand_query_context(user_query)
    
    # Step 2: Initialize Agent Orchestration Orchestrator
    engine = AgenticWorkflowEngine()
    
    # Step 3: Run Intent Routing Node
    print("[2/4] Triggering Asynchronous Intent Classification Node...")
    intent, router_audit = await engine.route_intent(expanded_prompt)
    print(f">> Selected Execution Pathway: {intent}")
    
    # Step 4: Conditionally dispatch execution flow based on classified intent
    print(f"[3/4] Dispatching Execution to Dedicated Target Agent Node...")
    if "STRATEGIC_ANALYTICS" in intent:
        final_output, agent_audit = await engine.execute_analytics(expanded_prompt)
    else:
        final_output, agent_audit = await engine.execute_data_tutor(expanded_prompt)
        
    print("\n[4/4] Automated Agent Processing Complete.")
    print("\n" + "="*50 + "\nFINAL COPILOT EXECUTIVE SUMMARY\n" + "="*50)
    print(final_output)
    print("="*50 + "\n")

if __name__ == "__main__":
    # Simulated enterprise B2B query containing shorthand acronyms
    sample_query = "Analyze our current MDF allocation adjustments vs last quarter's VCM thresholds."
    asyncio.run(run_copilot_pipeline(sample_query))