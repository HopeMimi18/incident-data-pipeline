# Incident Data Pipeline & Analytics

A compact Data Engineering project that ingests fictional incident data, cleans and validates it, loads it into SQLite, and exposes SQL analytics through a Streamlit dashboard.

## What this project demonstrates

- CSV ingestion
- Data validation and quality rules
- Missing-value handling
- Date parsing and rejection of invalid records
- Category standardisation
- Duplicate removal
- Derived analytical fields
- ETL pipeline design
- Relational loading into SQLite
- SQL analytics
- Pipeline-run metadata
- Automated tests
- GitHub Actions CI
- Streamlit dashboard

## Architecture

```text
Raw CSV
   |
   v
Extract
   |
   v
Transform
- validate dates
- normalise severity/status
- fill missing descriptive values
- remove duplicates
- derive analytics fields
   |
   v
Load
   |
   +--> cleaned_incidents.csv
   |
   +--> SQLite incidents.db
             |
             v
          SQL analytics
             |
             v
      Streamlit dashboard
```

## Project structure

```text
incident-data-pipeline/
├── .github/workflows/tests.yml
├── data/raw_incidents.csv
├── sql/
│   ├── analytics.sql
│   └── schema.sql
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── extract.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── tests/
│   ├── test_pipeline.py
│   └── test_transform.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Dataset

The included dataset is fictional and intentionally contains data-quality problems: inconsistent severity labels, inconsistent status casing, missing department/location values, a duplicate incident ID, an invalid date, and one row with a missing incident ID.

## Windows setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the ETL pipeline

```powershell
python -m src.pipeline
```

Expected result with the included dataset:

```text
Incident Data Pipeline completed successfully.
Input rows:          22
Rejected rows:       2
Duplicates removed:  1
Loaded rows:         19
```

The pipeline creates `data/cleaned_incidents.csv` and `data/incidents.db`.

## Run tests

```powershell
pytest -q
```

## Run the dashboard

```powershell
python -m streamlit run dashboard.py
```

Open `http://localhost:8501`.

## Transformation rules

Severity values are standardised to `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. Status values are standardised to `OPEN`, `IN_REVIEW`, `CLOSED`, or `RESOLVED`.

Rows are rejected if `incident_id` is missing or `reported_at` cannot be parsed. When the same incident ID appears more than once, the latest record is kept.

## Database tables

`incidents` stores the cleaned analytical dataset. `pipeline_runs` stores operational metadata for each ETL run: timestamp, input rows, rejected rows, duplicates removed, and output rows.

## Example analytics

The SQL layer answers questions such as:

- How many incidents occurred at each severity level?
- Which departments report the most incidents?
- Which incident types occur most often?
- Which high-priority incidents are still open or under review?
- How many incidents occurred per month?

See `sql/analytics.sql`.

## Testing

Automated tests cover severity standardisation, missing-value handling, invalid-date rejection, duplicate resolution, and end-to-end ETL loading into SQLite. GitHub Actions runs the tests on pushes and pull requests.

## Future improvements

- PostgreSQL instead of SQLite
- Incremental loading
- Scheduled pipelines
- Data-quality thresholds and alerts
- S3 raw/processed data layers
- AWS Glue / Athena
- Airflow or AWS Step Functions orchestration

## Author

Hope Lekgeu — WeThinkCode_ Software Engineering Student

## Disclaimer

All incident records in this repository are fictional and are provided only for educational and demonstration purposes.
