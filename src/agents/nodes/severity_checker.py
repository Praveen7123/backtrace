import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, SeverityOutput
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(SeverityOutput)

def severity_checker_node(state: IncidentState) -> IncidentState:
    print("Node 6: Checking severity...")

    prompt = f"""
    You are a DevOps severity assessment specialist.
    
    Assess the severity of this incident:
    
    Server: {state['server_name']}
    Root Cause: {state['root_cause']}
    Log Findings: {state['log_findings']}
    
    Severity levels:
    - low      → minor issue, no user impact
    - medium   → some impact, can wait for business hours
    - high     → significant impact, fix within 1 hour
    - critical → production down, fix immediately
    
    Assign severity and decide if escalation is needed.
    Escalate if severity is high or critical.
    """
    result = structured_llm.invoke(prompt)

    return {
        **state,
        "severity": result.severity,
        "escalation_needed": result.escalation_needed,
        "escalation_reason": result.reason
    }