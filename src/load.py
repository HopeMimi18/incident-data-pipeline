from pathlib import Path
import sqlite3
from datetime import datetime, timezone
import pandas as pd


def load_to_sqlite(df: pd.DataFrame, db_path: str | Path, quality: dict) -> None:
    """Load cleaned incidents and pipeline metadata into SQLite."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        load_df = df.copy()
        load_df["is_high_priority"] = load_df["is_high_priority"].astype(int)
        load_df.to_sql("incidents", conn, if_exists="replace", index=False)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TEXT NOT NULL,
                input_rows INTEGER NOT NULL,
                rejected_rows INTEGER NOT NULL,
                duplicates_removed INTEGER NOT NULL,
                output_rows INTEGER NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO pipeline_runs (
                run_timestamp, input_rows, rejected_rows,
                duplicates_removed, output_rows
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            quality["input_rows"], quality["rejected_rows"],
            quality["duplicates_removed"], quality["output_rows"],
        ))
        conn.commit()
