import pandas as pd

SEVERITY_MAP = {
    "low": "LOW", "medium": "MEDIUM", "med": "MEDIUM",
    "moderate": "MEDIUM", "high": "HIGH", "severe": "HIGH",
    "critical": "CRITICAL", "urgent": "CRITICAL",
}

STATUS_MAP = {
    "open": "OPEN", "in review": "IN_REVIEW", "in_review": "IN_REVIEW",
    "closed": "CLOSED", "resolved": "RESOLVED",
}


def transform_incidents(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean, validate and enrich incident data."""
    working = df.copy()
    input_rows = len(working)
    working.columns = [c.strip().lower() for c in working.columns]

    for column in [
        "incident_id", "department", "location", "incident_type",
        "severity", "status", "description"
    ]:
        working[column] = working[column].fillna("").astype(str).str.strip()

    working["reported_at"] = pd.to_datetime(
        working["reported_at"], errors="coerce", format="mixed", dayfirst=True
    )
    working["severity"] = working["severity"].str.lower().map(SEVERITY_MAP).fillna("UNKNOWN")
    working["status"] = working["status"].str.lower().map(STATUS_MAP).fillna("UNKNOWN")

    working["department"] = working["department"].replace("", "Unknown")
    working["location"] = working["location"].replace("", "Unknown")
    working["incident_type"] = working["incident_type"].replace("", "Unknown")
    working["description"] = working["description"].replace("", "Not specified")

    invalid = working["incident_id"].eq("") | working["reported_at"].isna()
    rejected_rows = int(invalid.sum())
    working = working.loc[~invalid].copy()

    working = working.sort_values("reported_at")
    before_dedup = len(working)
    working = working.drop_duplicates(subset=["incident_id"], keep="last")
    duplicates_removed = before_dedup - len(working)

    working["reported_date"] = working["reported_at"].dt.date.astype(str)
    working["year"] = working["reported_at"].dt.year.astype(int)
    working["month"] = working["reported_at"].dt.strftime("%Y-%m")
    working["is_high_priority"] = working["severity"].isin(["HIGH", "CRITICAL"])
    working = working.sort_values("reported_at").reset_index(drop=True)

    quality = {
        "input_rows": input_rows,
        "rejected_rows": rejected_rows,
        "duplicates_removed": int(duplicates_removed),
        "output_rows": len(working),
    }
    return working, quality
