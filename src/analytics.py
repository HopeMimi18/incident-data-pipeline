from pathlib import Path
import sqlite3
import pandas as pd


def _query(db_path: str | Path, sql: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn)


def incidents_by_severity(db_path):
    return _query(db_path, """
        SELECT severity, COUNT(*) AS incident_count
        FROM incidents GROUP BY severity
        ORDER BY incident_count DESC, severity
    """)


def incidents_by_department(db_path):
    return _query(db_path, """
        SELECT department, COUNT(*) AS incident_count
        FROM incidents GROUP BY department
        ORDER BY incident_count DESC, department
    """)


def incidents_by_type(db_path):
    return _query(db_path, """
        SELECT incident_type, COUNT(*) AS incident_count
        FROM incidents GROUP BY incident_type
        ORDER BY incident_count DESC, incident_type
    """)


def high_priority_open_incidents(db_path):
    return _query(db_path, """
        SELECT incident_id, reported_at, department, location,
               incident_type, severity, status
        FROM incidents
        WHERE is_high_priority = 1
          AND status IN ('OPEN', 'IN_REVIEW')
        ORDER BY reported_at DESC
    """)
