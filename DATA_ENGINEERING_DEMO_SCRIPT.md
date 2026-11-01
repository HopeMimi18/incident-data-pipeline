# Data Engineering Demo Script (6–8 minutes)

`WTC-88WSVTXV`
## LMS Tracking

**WeThinkCode_ Tracking Code:** `WTC-88WSVTXV`

## 1. Introduction — 30–45 seconds

“Hi, I’m Hope Lekgeu. This is my Data Engineering project, Incident Data Pipeline & Analytics.

The problem I’m solving is that raw operational data is often inconsistent. It may contain missing fields, duplicate records, invalid dates and inconsistent categories. My project builds an ETL pipeline that turns that raw data into a clean analytical dataset.”

## 2. Architecture — 45 seconds

Show the README architecture.

“The source is a CSV file. The Extract step reads the raw data. The Transform step validates and cleans it. The Load step stores the clean result in both a CSV output and a SQLite database. SQL queries and a Streamlit dashboard are then used for analysis.”

## 3. Show the dirty source data — 60 seconds

Open `data/raw_incidents.csv`.

“I intentionally included data-quality problems: different severity labels such as moderate, med and severe; inconsistent status values; missing department and location values; a duplicate incident; an invalid date; and one row with no incident ID.”

## 4. Transformation logic — 60–90 seconds

Open `src/transform.py`.

“The transformation stage standardises severity and status values, parses dates, fills non-critical missing values, rejects unusable rows, removes duplicate incident IDs by keeping the latest record, and creates derived fields such as month and high-priority status.”

## 5. Run the ETL pipeline — 60 seconds

Run:

```powershell
python -m src.pipeline
```

Explain the result:

“The pipeline reports how many records came in, how many were rejected, how many duplicates were removed and how many clean rows were loaded. This provides basic data-quality observability.”

## 6. Database + SQL — 60 seconds

Show `sql/analytics.sql`.

“The clean dataset is loaded into SQLite. I can query incidents by severity, department and incident type, and identify high-priority incidents that are still open.”

## 7. Dashboard — 60–90 seconds

Run:

```powershell
python -m streamlit run dashboard.py
```

Show metrics, charts and high-priority incidents.

“The dashboard is not the core of the project; it is the presentation layer over the engineered data. The important part is that all visuals come from the cleaned database rather than directly from the dirty CSV.”

## 8. Automated testing — 45 seconds

Run:

```powershell
pytest -q
```

“The automated tests verify severity standardisation, missing-value handling, invalid-date rejection, duplicate resolution and end-to-end database loading.”

## 9. Closing — 30 seconds

“This project demonstrates the full Data Engineering lifecycle: ingestion, validation, transformation, relational storage, SQL analytics, data-quality evidence and automated testing.

Future improvements would include PostgreSQL, scheduled pipelines, incremental loading, S3 data layers and orchestration using services such as AWS Glue, Athena or Step Functions.”
