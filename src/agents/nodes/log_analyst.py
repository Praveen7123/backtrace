import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, LogAnalysisOutput
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(LogAnalysisOutput)

def log_analyst_node(state: IncidentState) -> IncidentState:
    print("Node 2: Analysing error log...")

    prompt = f"""
    You are a senior DevOps engineer specializing in log analysis.
    
    Analyse this error log from server {state['server_name']} 
    at {state['incident_time']}:
    
    {state['error_log']}
    
    Find:
    1. Key error patterns and stack traces
    2. Type of error (memory, cpu, network, database, unknown)
    3. When the error first appeared in the log
    
    Be specific and technical.
    """

    result = structured_llm.invoke(prompt)

    return {
        **state,
        "log_findings": f"Findings: {result.findings}\nError Type: {result.error_type}\nTimeline: {result.timeline}"
    }
