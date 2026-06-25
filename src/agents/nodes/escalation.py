import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)

def escalation_node(state: IncidentState) -> IncidentState:
    print("Node 7: Escalating incident...")

    prompt = f"""
    You are an incident commander handling a critical escalation.
    
    Incident Details:
    Server: {state['server_name']}
    Severity: {state['severity']}
    Root Cause: {state['root_cause']}
    Escalation Reason: {state['escalation_reason']}
    
    Write a concise escalation notice that includes:
    1. What is down and since when
    2. Root cause identified
    3. Who needs to be paged immediately
    4. Immediate actions to take in next 15 minutes
    
    Keep it short and urgent.
    """

    result = llm.invoke(prompt)

    return {
        **state,
        "escalation_reason": f"ESCALATED:\n{result.content}"
    }