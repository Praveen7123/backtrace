#what basically this code does is it provides a whiteboard every agent reads from it 
#The incident state seperate for multiagents and each class handles how the output is structured up same for all..

from typing import TypedDict,Optional

from pydantic import BaseModel,Field

class IncidentState(TypedDict):

    #inputs we feed into
    server_name:str
    error_log:str
    incident_time:str
    github_repo:str
 
    #outputs for the nodes
    is_valid:bool
    validation_message:str

    log_findings:str
    db_findings:str
    doc_findings:str

    root_cause:str
    severity:str

    escalation_needed:bool
    escalation_reason:str

    work_order:str
    assigned_team:str

    github_findings:str
    commit_hash:str

    final_report:str


class ValidationOutput(BaseModel):
    is_valid:bool = Field(description="True if all inputs are present and valid")
    message:str = Field(description="Reason if i valid,confirmation if valid")

class LogAnalysisOutput(BaseModel):
    findings:str = Field(description="Key patterns and errors found in the log")
    error_type:str = Field(description="Type:memory,cpu,network,database,unknown")
    timeline:str = Field(description="When the error first appeared")

class DBInspectionOutput(BaseModel):
    findings:str = Field(description="Relevant past incidents and deployments found")
    past_incidents:str = Field(description="Similar past incidents on this server")
    recent_deployments:str = Field(description="Deployments close to incident time")

class DocRetrievalOutput(BaseModel):
    findings:str = Field(description="Relevant runbook content found")
    recommended_fix:str = Field(description="Fix suggested by the runbook")

class RootCauseOutput(BaseModel):
    root_cause:str=Field(description="Root cause in one clear sentence")
    evidence:str=Field(description="Evidence from logs,DB and docs")
    confidence:float = Field(description="Confidence score between 0.0 and 1.0")

class SeverityOutput(BaseModel):
    severity:str=Field(description="One of:low,medium,high,critical")
    escalation_needed:bool = Field(description="True if severity is high or critical")
    reason:str = Field(description="Why this severity was assigned")

class WorkOrderOutput(BaseModel):
    steps:str = Field(description="Step by step fix instructions")
    assigned_team:str = Field(description="True if severity is high or critical")
    reason:str = Field(description="Why this severity was assigned")

class GitHubOutput(BaseModel):
    findings:str = Field(description="Which commit likely caused the incident")
    commit_hash:str = Field(description="Who made the commit")
    author:str = Field(description="Files change in that commit")


class FinalReportOutput(BaseModel):
    summary:str = Field(description="One paragraph summary of the full investigation")
    root_cause:str = Field(description="Final confirmed root cause")
    fix_applied:str = Field(description="What fix was recommended")
    assigned_team:str = Field(description="Team assigned to fix")
    severity:str = Field(description="Final severity level")
