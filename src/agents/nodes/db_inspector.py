import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, DBInspectionOutput
from src.tools.db_tools import get_server_info, get_past_incidents, get_recent_deployments
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(DBInspectionOutput)

def db_inspector_node(state: IncidentState) -> IncidentState:
    print("Node 3: Inspecting database...")

    server_info = get_server_info.invoke({"server_name": state['server_name']})
    past_incidents = get_past_incidents.invoke({"server_name": state['server_name']})
    recent_deployments = get_recent_deployments.invoke({"server_name": state['server_name']})

    prompt = f"""
    You are a DevOps database analyst.
    
    Analyse this data for server {state['server_name']}:
    
    Server Info:
    {server_info}
    
    Past Incidents:
    {past_incidents}
    
    Recent Deployments:
    {recent_deployments}
    
    Current incident time: {state['incident_time']}
    Current error: {state['log_findings']}
    
    Find:
    1. Any patterns in past incidents
    2. Suspicious deployments close to incident time
    3. Is this a recurring issue?
    """

    result = structured_llm.invoke(prompt)

    return {
        **state,
        "db_findings": f"Findings: {result.findings}\nPast Incidents: {result.past_incidents}\nDeployments: {result.recent_deployments}"
    }