import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState,ValidationOutput
from config import GROQ_API_KEY,GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(ValidationOutput)

def validator_node(state:IncidentState)->IncidentState:
    print("Node 1: Validating input...")
    prompt = f"""
    You are an input validator for a DevOps incident system.
    
    Check if the following inputs are valid and complete:
    - Server Name: {state['server_name']}
    - Error Log: {state['error_log']}
    - Incident Time: {state['incident_time']}
    - GitHub Repo: {state['github_repo']}
    
    Rules:
    - server_name must not be empty
    - error_log must contain actual error information
    - incident_time must be a valid time format
    - github_repo is OPTIONAL. An empty github_repo is perfectly valid.
      Only treat it as invalid if it is non-empty AND not in the
      "username/repo" format. Never fail validation just because it is empty.

    Set is_valid to true if all the required inputs (server_name, error_log,
    incident_time) are valid, regardless of whether github_repo is provided.

    Validate and respond.
    """
    result = structured_llm.invoke(prompt)

    return {
        **state,
        "is_valid": result.is_valid,
        "validation_message": result.message
    }

