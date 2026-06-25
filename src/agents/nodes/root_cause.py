import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, RootCauseOutput
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(RootCauseOutput)

def root_cause_node(state: IncidentState) -> IncidentState:
    print("Node 5: Finding root cause...")

    prompt = f"""
    You are a senior SRE (Site Reliability Engineer).
    
    Combine ALL findings below to identify the definitive root cause:
    
    Server: {state['server_name']}
    Incident Time: {state['incident_time']}
    
    Log Analysis:
    {state['log_findings']}
    
    Database Findings:
    {state['db_findings']}
    
    Runbook Findings:
    {state['doc_findings']}
    
    GitHub Findings:
    {state['github_findings']}
    
    Identify:
    1. The single root cause in one clear sentence
    2. Evidence supporting this conclusion
    3. Your confidence level (0.0 to 1.0)
    """
    result = structured_llm.invoke(prompt)
    return {
        **state,
        "root_cause": f"{result.root_cause}\nEvidence: {result.evidence}\nConfidence: {result.confidence}"
    }