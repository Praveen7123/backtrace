import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.tools import tool
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

@tool
def get_server_info(server_name:str) -> str:
    """Get basic information about a server including environment, team and region."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
         "SELECT * FROM servers WHERE server_name = ?", (server_name,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return f"No server found with name: {server_name}"

    return f"Server {row[1]}: environment={row[2]}, team={row[3]}, region={row[4]}"

@tool
def get_recent_deployments(server_name: str) -> str:
    """Get recent deployments for a server to find changes close to the incident time."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT version, deployed_by, timestamp, status FROM deployments WHERE server_name = ? ORDER BY timestamp DESC LIMIT 5",
        (server_name,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return f"No recent deployments found for: {server_name}"

    result = f"Recent deployments for {server_name}:\n"
    for row in rows:
        result += f"- [{row[2]}] {row[0]} by {row[1]} → {row[3]}\n"
    return result

@tool
def get_past_incidents(server_name: str) -> str:
    """Get past incidents for a server to find recurring patterns."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT error_type, description, timestamp, fix_applied FROM incidents WHERE server_name = ? ORDER BY timestamp DESC LIMIT 5",
        (server_name,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return f"No past incidents found for: {server_name}"

    result = f"Past incidents for {server_name}:\n"
    for row in rows:
        result += f"- [{row[2]}] {row[0]}: {row[1]} → Fix: {row[3]}\n"
    return result

@tool
def get_all_servers() -> str:
    """Get list of all servers to check for cascade failures across multiple servers."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT server_name, environment, team FROM servers")
    rows = cursor.fetchall()
    conn.close()

    result = "All servers:\n"
    for row in rows:
        result += f"- {row[0]} ({row[1]}) → Team: {row[2]}\n"
    return result
