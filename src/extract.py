from pathlib import Path
import pandas as pd


def extract_csv(path: str | Path) -> pd.DataFrame:
    """Read raw incident data from CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    df = pd.read_csv(path, dtype=str)
    if df.empty:
        raise ValueError("Input dataset is empty.")
    return df
