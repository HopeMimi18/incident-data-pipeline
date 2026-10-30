CREATE TABLE incidents (
    incident_id TEXT PRIMARY KEY,
    reported_at TEXT NOT NULL,
    department TEXT NOT NULL,
    location TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT NOT NULL,
    reported_date TEXT NOT NULL,
    year INTEGER NOT NULL,
    month TEXT NOT NULL,
    is_high_priority INTEGER NOT NULL
);

CREATE TABLE pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_timestamp TEXT NOT NULL,
    input_rows INTEGER NOT NULL,
    rejected_rows INTEGER NOT NULL,
    duplicates_removed INTEGER NOT NULL,
    output_rows INTEGER NOT NULL
);
