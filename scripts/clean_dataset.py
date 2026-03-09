"""Clean and validate the marketing dataset for downstream analysis."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RAW_CSV_FILENAME = "marketing_campaign_dataset.csv"
OUTPUT_CSV_FILENAME = "marketing_campaign_dataset_cleaned.csv"


REQUIRED_COLUMNS: list[str] = [
    "Campaign_ID",
    "Company",
    "Campaign_Type",
    "Target_Audience",
    "Duration",
    "Channel_Used",
    "Conversion_Rate",
    "Acquisition_Cost",
    "ROI",
    "Location",
    "Language",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "Customer_Segment",
    "Date",
]


def clean_dataset(
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load, clean, deduplicate, and save the marketing dataset."""
    if input_path is None:
        source_path = Path(__file__).resolve().parent.parent / "datasets" / RAW_CSV_FILENAME
    else:
        source_path = Path(input_path)

    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {source_path}")

    try:
        df = pd.read_csv(source_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to load CSV file '{source_path}': {exc}") from exc

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    acquisition_clean = (
        df["Acquisition_Cost"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    )
    df["Acquisition_Cost"] = pd.to_numeric(acquisition_clean, errors="coerce").astype(float)

    duration_clean = df["Duration"].astype(str).str.replace(" days", "", regex=False).str.strip()
    df["Duration"] = pd.to_numeric(duration_clean, errors="coerce").astype("Int64")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.drop_duplicates().reset_index(drop=True)

    if output_path is None:
        destination = Path(__file__).resolve().parent.parent / "datasets" / OUTPUT_CSV_FILENAME
    else:
        destination = Path(output_path)

    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return df


if __name__ == "__main__":
    cleaned_df = clean_dataset()
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    print("Saved cleaned file to: datasets/marketing_campaign_dataset_cleaned.csv")
