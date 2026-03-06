"""Utilities for cleaning the marketing campaign dataset for downstream analytics."""

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


def clean_marketing_data(file_path: str | Path | None = None) -> pd.DataFrame:
    """Load, clean, deduplicate, and save the marketing campaign dataset.

    Steps performed:
    1. Load CSV data from ``file_path`` or ``dataset/marketing_campaign_dataset.csv`` when omitted.
    2. Clean ``Acquisition_Cost`` by removing ``$`` and ``,`` and converting to float.
    3. Clean ``Duration`` by removing `` days`` and converting to integer.
    4. Convert ``Date`` to pandas datetime.
    5. Remove duplicate rows.
    6. Save cleaned output as ``dataset/marketing_campaign_dataset_cleaned.csv``.

    Args:
        file_path: Optional path to the raw input CSV file. If ``None``, the
            default is ``dataset/marketing_campaign_dataset.csv``.

    Returns:
        A cleaned pandas DataFrame.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If required columns are missing or critical parsing fails.
        RuntimeError: If data cannot be loaded or saved.
    """
    if file_path is None:
        source_path = Path(__file__).resolve().parent.parent / "dataset" / RAW_CSV_FILENAME
    else:
        source_path = Path(file_path)

    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {source_path}")

    try:
        df = pd.read_csv(source_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to load CSV file '{source_path}': {exc}") from exc

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    try:
        acquisition_clean = (
            df["Acquisition_Cost"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        )
        df["Acquisition_Cost"] = pd.to_numeric(acquisition_clean, errors="coerce").astype(float)

        duration_clean = df["Duration"].astype(str).str.replace(" days", "", regex=False).str.strip()
        df["Duration"] = pd.to_numeric(duration_clean, errors="coerce").astype("Int64")

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        # Replace inf values with NaN to keep downstream BI ingestion stable.
        df = df.replace([np.inf, -np.inf], np.nan)

        df = df.drop_duplicates().reset_index(drop=True)
    except Exception as exc:
        raise ValueError(f"Failed while cleaning dataset columns: {exc}") from exc

    output_dir = Path(__file__).resolve().parent.parent / "dataset"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_CSV_FILENAME

    try:
        df.to_csv(output_path, index=False)
    except Exception as exc:
        raise RuntimeError(f"Failed to save cleaned CSV to '{output_path}': {exc}") from exc

    return df


if __name__ == "__main__":
    cleaned_df = clean_marketing_data()
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    print("Saved cleaned file to: dataset/marketing_campaign_dataset_cleaned.csv")
