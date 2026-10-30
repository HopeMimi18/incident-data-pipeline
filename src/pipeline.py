from pathlib import Path
from src.extract import extract_csv
from src.transform import transform_incidents
from src.load import load_to_sqlite

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw_incidents.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "cleaned_incidents.csv"
DB_PATH = PROJECT_ROOT / "data" / "incidents.db"


def run_pipeline(raw_path=RAW_PATH, clean_path=CLEAN_PATH, db_path=DB_PATH) -> dict:
    raw_df = extract_csv(raw_path)
    clean_df, quality = transform_incidents(raw_df)
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(clean_path, index=False)
    load_to_sqlite(clean_df, db_path, quality)
    return quality


if __name__ == "__main__":
    result = run_pipeline()
    print("Incident Data Pipeline completed successfully.")
    print(f"Input rows:          {result['input_rows']}")
    print(f"Rejected rows:       {result['rejected_rows']}")
    print(f"Duplicates removed:  {result['duplicates_removed']}")
    print(f"Loaded rows:         {result['output_rows']}")
