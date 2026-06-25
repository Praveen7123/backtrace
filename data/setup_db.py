import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from config import DB_PATH

def setup_database():
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #SERVERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers(
    id INTEGER PRIMARY KEY,
    server_name TEXT UNIQUE,
    environment TEXT,
    team TEXT,
    region TEXT
    )
    """)

    #PAST INCIDENTS
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS incidents(
        id INTERGER PRIMARY KEY,
        server_name TEXT,
        error_type TEXT,
        description TEXT,
        timestamp TEXT,
        resolved_by TEXT,
        fix_applied TEXT
        )
        """
    )

    #deployments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deployments(
    id INTEGER PRIMARY KEY,
    server_name TEXT,
    version TEXT,
    deployed_by TEXT,
    timestamp TEXT,
    status TEXT
    )
    """
    )

    servers = [
         ("prod-01", "production", "backend-team", "us-east-1"),
         ("prod-02", "production", "frontend-team", "us-east-1"),
         ("prod-03", "production", "infra-team", "us-west-2"),
         ("staging-01", "staging", "devops-team", "us-east-1"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO servers VALUES (NULL,?,?,?,?)",servers
    )

    incidents = [
        ("prod-01", "OutOfMemoryError", "Heap exhausted after deployment", "2024-01-15 14:23", "backend-team", "Increased heap size, fixed memory leak"),
        ("prod-01", "CPU Spike", "Runaway process after config change", "2024-02-03 09:10", "infra-team", "Killed process, rolled back config"),
        ("prod-02", "Database Connection Timeout", "Connection pool exhausted", "2024-02-20 16:45", "database-team", "Increased pool size"),
        ("prod-03", "Disk Full", "Logs not rotated for 30 days", "2024-03-01 08:00", "infra-team", "Log rotation enabled"),
        ("prod-01", "OutOfMemoryError", "Memory leak resurfaced", "2024-03-10 11:30", "backend-team", "Permanent fix deployed"),
        ("prod-02", "CPU Spike", "High traffic during sale event", "2024-03-15 18:00", "infra-team", "Scaled horizontally"),
        ("prod-03", "Network Timeout", "DNS misconfiguration", "2024-04-01 07:00", "network-team", "Fixed DNS settings"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO incidents VALUES (NULL,?,?,?,?,?,?)", incidents
    )

    deployments = [
        ("prod-01", "v2.3.0", "team-backend", "2024-03-10 09:00", "success"),
        ("prod-01", "v2.3.1", "team-backend", "2024-03-10 13:45", "success"),
        ("prod-01", "v2.3.2", "team-backend", "2024-03-10 15:00", "failed"),
        ("prod-02", "v1.0.0", "team-frontend", "2024-03-10 09:00", "success"),
        ("prod-02", "v1.1.0", "team-frontend", "2024-03-15 17:00", "success"),
        ("prod-03", "v4.1.0", "team-infra", "2024-03-10 14:00", "success"),
        ("staging-01", "v2.3.2", "team-devops", "2024-03-09 16:00", "success"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO deployments VALUES (NULL,?,?,?,?,?)", deployments
    )

    conn.commit()
    conn.close()
    print("Database setup is completed")
    print(f"DB created at:{DB_PATH}")

if __name__ == "__main__":
    setup_database()