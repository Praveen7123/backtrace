import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from langchain_groq import ChatGroq
from src.schemas.schemas import IncidentState, DocRetrievalOutput
from src.tools.rag_tools import search_runbooks, search_past_postmortems
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(DocRetrievalOutput)

def doc_retriever_node(state: IncidentState) -> IncidentState:
    print("Node 4: Searching runbooks...")
    runbook_results = search_runbooks.invoke({"query": state['log_findings']})
    postmortem_results = search_past_postmortems.invoke({"query": state['log_findings']})

    prompt = f"""
    You are a DevOps documentation specialist.
    
    Based on this incident:
    Server: {state['server_name']}
    Log Findings: {state['log_findings']}
    
    Runbook content found:
    {runbook_results}
    
    Past postmortems found:
    {postmortem_results}
    
    Extract:
    1. Most relevant fix procedure from runbooks
    2. Any matching past incidents and how they were resolved
    """

    result = structured_llm.invoke(prompt)

    return {
        **state,
        "doc_findings": f"Findings: {result.findings}\nRecommended Fix: {result.recommended_fix}"
    }