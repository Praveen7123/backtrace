import os
import sys

# Ensure UTF-8 output so emoji/unicode print on Windows consoles (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graph.graph import incident_graph
from src.rag.setup_rag import setup_rag
from data.setup_db import setup_database


def run_incident(
    server_name: str,
    error_log: str,
    incident_time: str,
    github_repo: str = ""
):
    print("\n" + "="*60)
    print("🚀 DEVOPS INCIDENT COPILOT")
    print("="*60)
    print(f"Server:  {server_name}")
    print(f"Time:    {incident_time}")
    print(f"Repo:    {github_repo or 'Not provided'}")
    print("="*60 + "\n")
    initial_state = {
        "server_name": server_name,
        "error_log": error_log,
        "incident_time": incident_time,
        "github_repo": github_repo,

        # empty — filled by nodes
        "is_valid": False,
        "validation_message": "",
        "log_findings": "",
        "db_findings": "",
        "doc_findings": "",
        "root_cause": "",
        "severity": "",
        "escalation_needed": False,
        "escalation_reason": "",
        "work_order": "",
        "assigned_team": "",
        "github_findings": "",
        "commit_hash": "",
        "final_report": ""
    }
    result = incident_graph.invoke(initial_state)
    print("\n" + "="*60)
    print("📊 INVESTIGATION COMPLETE")
    print("="*60)
    print(f"\nValidation:     {result['validation_message']}")
    print(f"\nLog Findings:\n{result['log_findings']}")
    print(f"\nDB Findings:\n{result['db_findings']}")
    print(f"\nDoc Findings:\n{result['doc_findings']}")
    print(f"\nRoot Cause:\n{result['root_cause']}")
    print(f"\nSeverity:      {result['severity']}")

    if result['escalation_needed']:
        print(f"\nEscalation:\n{result['escalation_reason']}")

    print(f"\nWork Order:\n{result['work_order']}")
    print(f"\nAssigned To:   {result['assigned_team']}")
    print("\n" + "="*60)

    return result


if __name__ == "__main__":
    print("Setting up database...")
    setup_database()

    print("Setting up RAG...")
    setup_rag()
    run_incident(
        server_name="prod-01",
        error_log="""
        2024-03-10 14:23:45 ERROR OutOfMemoryError: Java heap space
            at java.util.Arrays.copyOf(Arrays.java:3210)
            at com.service.MemoryManager.allocate(MemoryManager.java:47)
            at com.service.RequestHandler.process(RequestHandler.java:123)
        2024-03-10 14:23:46 ERROR GC overhead limit exceeded
        2024-03-10 14:23:47 FATAL Service crashed - restarting
        2024-03-10 14:24:01 ERROR Service failed to restart - heap still exhausted
        """,
        incident_time="2024-03-10 14:23:45",
        github_repo=""
    )