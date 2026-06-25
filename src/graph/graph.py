import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langgraph.graph import StateGraph, END
from src.schemas.schemas import IncidentState
from src.agents.nodes.validator import validator_node
from src.agents.nodes.log_analyst import log_analyst_node
from src.agents.nodes.db_inspector import db_inspector_node
from src.agents.nodes.doc_retriever import doc_retriever_node
from src.agents.nodes.root_cause import root_cause_node
from src.agents.nodes.severity_checker import severity_checker_node
from src.agents.nodes.escalation import escalation_node
from src.agents.nodes.work_order import work_order_node


def should_escalate(state: IncidentState) -> str:
    """Decides whether to escalate or go straight to work order."""
    if state.get("escalation_needed", False):
        return "escalate"
    return "work_order"


def is_valid_input(state: IncidentState) -> str:
    """Decides whether to continue or stop if input is invalid."""
    if state.get("is_valid", False):
        return "continue"
    return "stop"


def build_graph():
    graph = StateGraph(IncidentState)
    graph.add_node("validator", validator_node)
    graph.add_node("log_analyst", log_analyst_node)
    graph.add_node("db_inspector", db_inspector_node)
    graph.add_node("doc_retriever", doc_retriever_node)
    graph.add_node("root_cause", root_cause_node)
    graph.add_node("severity_checker", severity_checker_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("work_order", work_order_node)
    graph.set_entry_point("validator")
    graph.add_conditional_edges(
        "validator",
        is_valid_input,
        {
            "continue": "log_analyst",
            "stop": END
        }
    )
    graph.add_edge("log_analyst", "db_inspector")
    graph.add_edge("db_inspector", "doc_retriever")
    graph.add_edge("doc_retriever", "root_cause")
    graph.add_edge("root_cause", "severity_checker")
    graph.add_conditional_edges(
        "severity_checker",
        should_escalate,
        {
            "escalate": "escalation",
            "work_order": "work_order"
        }
    )
    graph.add_edge("escalation", "work_order")
    graph.add_edge("work_order", END)

    return graph.compile()

incident_graph = build_graph()