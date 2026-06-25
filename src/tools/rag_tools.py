import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.tools import tool
from src.rag.setup_rag import get_retriever

@tool
def search_runbooks(query: str) -> str:
    """Search server runbooks for fixes and procedures related to the query."""
    retriever = get_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant runbook content found."

    result = "Relevant runbook content:\n\n"
    for i, doc in enumerate(docs, 1):
        result += f"[Chunk {i}]:\n{doc.page_content}\n\n"
    return result

@tool
def search_past_postmortems(query: str) -> str:
    """Search past incident postmortems for similar issues and their fixes."""
    retriever = get_retriever()
    docs = retriever.invoke(f"past incident postmortem {query}")

    if not docs:
        return "No relevant postmortems found."

    result = "Relevant past postmortems:\n\n"
    for i, doc in enumerate(docs, 1):
        result += f"[Postmortem {i}]:\n{doc.page_content}\n\n"
    return result