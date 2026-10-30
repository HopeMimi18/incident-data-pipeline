from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
from src.analytics import (
    incidents_by_department, incidents_by_severity,
    incidents_by_type, high_priority_open_incidents,
)
from src.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "incidents.db"

st.set_page_config(page_title="Incident Data Pipeline", page_icon="📊", layout="wide")
st.title("📊 Incident Data Engineering Dashboard")
st.caption("Fictional incident data • ETL • SQLite • SQL analytics")

if st.button("Run ETL Pipeline", type="primary"):
    result = run_pipeline()
    st.success(
        f"Pipeline complete: {result['output_rows']} rows loaded, "
        f"{result['rejected_rows']} rejected, "
        f"{result['duplicates_removed']} duplicate removed."
    )

if not DB_PATH.exists():
    st.info("Run the ETL pipeline first.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    incidents = pd.read_sql_query("SELECT * FROM incidents", conn)
    runs = pd.read_sql_query(
        "SELECT * FROM pipeline_runs ORDER BY run_id DESC LIMIT 5", conn
    )

c1, c2, c3, c4 = st.columns(4)
c1.metric("Clean incidents", len(incidents))
c2.metric("High priority", int(incidents["is_high_priority"].sum()))
c3.metric("Open / In review", int(incidents["status"].isin(["OPEN", "IN_REVIEW"]).sum()))
c4.metric("Departments", incidents["department"].nunique())

st.subheader("Incidents by severity")
st.bar_chart(incidents_by_severity(DB_PATH).set_index("severity"))
st.subheader("Incidents by department")
st.bar_chart(incidents_by_department(DB_PATH).set_index("department"))
st.subheader("Incident types")
st.dataframe(incidents_by_type(DB_PATH), use_container_width=True)
st.subheader("High-priority open incidents")
st.dataframe(high_priority_open_incidents(DB_PATH), use_container_width=True)
st.subheader("Recent pipeline runs")
st.dataframe(runs, use_container_width=True)
with st.expander("View cleaned dataset"):
    st.dataframe(incidents, use_container_width=True)
st.caption("This project uses fictional data for learning and demonstration.")
