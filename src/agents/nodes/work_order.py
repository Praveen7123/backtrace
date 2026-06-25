import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, WorkOrderOutput
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(WorkOrderOutput)

def work_order_node(state: IncidentState) -> IncidentState:
    print("Node 8: Generating work order...")

    prompt = f"""
    You are a DevOps work order specialist.
    
    Create a detailed work order for this incident:
    
    Server: {state['server_name']}
    Root Cause: {state['root_cause']}
    Severity: {state['severity']}
    Recommended Fix from Runbook: {state['doc_findings']}
    GitHub Findings: {state['github_findings']}
    
    Generate:
    1. Step by step fix instructions (numbered)
    2. Which team should handle this
    3. Estimated time to fix
    
    Be specific and actionable.
    """

    result = structured_llm.invoke(prompt)

    return {
        **state,
        "work_order": result.steps,
        "assigned_team": result.assigned_team
    }