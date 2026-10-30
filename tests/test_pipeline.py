from pathlib import Path
import sqlite3
from src.pipeline import run_pipeline


def test_pipeline_loads_clean_data(tmp_path: Path):
    raw = tmp_path / "raw.csv"
    clean = tmp_path / "clean.csv"
    db = tmp_path / "incidents.db"

    raw.write_text(
        "incident_id,reported_at,department,location,incident_type,severity,status,description\n"
        "X1,2026-10-01 08:00,IT,Office,Cut,high,open,Example\n",
        encoding="utf-8",
    )

    result = run_pipeline(raw, clean, db)
    assert result["output_rows"] == 1
    assert clean.exists()
    assert db.exists()

    with sqlite3.connect(db) as conn:
        count = conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
    assert count == 1
