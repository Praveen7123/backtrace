"""FastAPI bridge that exposes the DevOps Incident Copilot pipeline over HTTP.

Run with:
    uvicorn api:app --reload --port 8000

The React frontend (in ../incident-portal) calls POST /investigate.
"""
import os
import sys
from contextlib import asynccontextmanager

# Ensure UTF-8 output so emoji/unicode print on Windows consoles (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.graph.graph import incident_graph
from src.rag.setup_rag import setup_rag
from data.setup_db import setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Prepare the database and RAG index once when the server boots.
    print("Setting up database...")
    setup_database()
    print("Setting up RAG...")
    setup_rag()
    print("DevOps Incident Copilot API ready.")
    yield


app = FastAPI(
    title="DevOps Incident Copilot API",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the Vite dev server (and any local frontend) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    server_name: str = Field(..., description="Name of the affected server, e.g. prod-01")
    error_log: str = Field(..., description="Raw error log text")
    incident_time: str = Field(..., description="When the incident occurred")
    github_repo: str = Field("", description="Optional 'username/repo'")


class IncidentResponse(BaseModel):
    server_name: str
    incident_time: str
    github_repo: str
    is_valid: bool
    validation_message: str
    log_findings: str
    db_findings: str
    doc_findings: str
    root_cause: str
    severity: str
    escalation_needed: bool
    escalation_reason: str
    work_order: str
    assigned_team: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/investigate", response_model=IncidentResponse)
def investigate(req: IncidentRequest):
    initial_state = {
        "server_name": req.server_name,
        "error_log": req.error_log,
        "incident_time": req.incident_time,
        "github_repo": req.github_repo,
        # empty — filled by the graph nodes
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
        "final_report": "",
    }

    result = incident_graph.invoke(initial_state)

    return IncidentResponse(
        server_name=req.server_name,
        incident_time=req.incident_time,
        github_repo=req.github_repo,
        is_valid=result.get("is_valid", False),
        validation_message=result.get("validation_message", ""),
        log_findings=result.get("log_findings", ""),
        db_findings=result.get("db_findings", ""),
        doc_findings=result.get("doc_findings", ""),
        root_cause=result.get("root_cause", ""),
        severity=result.get("severity", ""),
        escalation_needed=result.get("escalation_needed", False),
        escalation_reason=result.get("escalation_reason", ""),
        work_order=result.get("work_order", ""),
        assigned_team=result.get("assigned_team", ""),
    )
