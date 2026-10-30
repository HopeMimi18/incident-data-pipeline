import pandas as pd
from src.transform import transform_incidents


def sample_row(**overrides):
    row = {
        "incident_id": "A1",
        "reported_at": "2026-10-01",
        "department": "IT",
        "location": "Office",
        "incident_type": "Cut",
        "severity": "low",
        "status": "open",
        "description": "Example",
    }
    row.update(overrides)
    return row


def test_severity_is_standardised():
    clean, quality = transform_incidents(pd.DataFrame([sample_row(severity="severe")]))
    assert clean.iloc[0]["severity"] == "HIGH"
    assert quality["output_rows"] == 1


def test_missing_department_is_filled():
    clean, _ = transform_incidents(pd.DataFrame([sample_row(department="")]))
    assert clean.iloc[0]["department"] == "Unknown"


def test_invalid_date_is_rejected():
    clean, quality = transform_incidents(pd.DataFrame([sample_row(reported_at="not-a-date")]))
    assert clean.empty
    assert quality["rejected_rows"] == 1


def test_duplicate_incident_keeps_latest_record():
    df = pd.DataFrame([
        sample_row(reported_at="2026-10-01 08:00", description="Older"),
        sample_row(reported_at="2026-10-01 09:00", severity="high", description="Latest"),
    ])
    clean, quality = transform_incidents(df)
    assert len(clean) == 1
    assert clean.iloc[0]["description"] == "Latest"
    assert quality["duplicates_removed"] == 1
