"""Reproducible script for notebook 01: initial exploration."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from download_dataset import download_kaggle_dataset


DEFAULT_DATASET = "raw_marketing_dataset.csv"


def resolve_input_path(repo_root: Path, dataset: str, input_path: str | None) -> Path:
    if input_path:
        path = Path(input_path)
        return path if path.is_absolute() else (repo_root / path).resolve()
    return (repo_root / "datasets" / dataset).resolve()


def print_saved_artifacts(artifacts: list[Path]) -> None:
    for artifact in artifacts:
        print(f"Saved: {artifact}")


def run_initial_exploration(
    input_csv: Path,
    results_dir: Path,
    download_if_missing: bool,
    force_download: bool,
    dataset_ref: str,
) -> None:
    if (not input_csv.exists() or force_download) and download_if_missing:
        imported_path = download_kaggle_dataset(dataset_ref=dataset_ref, csv_name=input_csv.name)
        print(f"Downloaded to: {imported_path}")

    if not input_csv.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_csv}")

    results_dir.mkdir(parents=True, exist_ok=True)
    df_raw = pd.read_csv(input_csv)

    missing_summary = (
        pd.DataFrame(
            {
                "missing_count": df_raw.isna().sum(),
                "missing_pct": (df_raw.isna().mean() * 100).round(4),
            }
        )
        .sort_values(["missing_count", "missing_pct"], ascending=False)
    )

    numeric_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
    numeric_profile = df_raw[numeric_cols].describe().T if numeric_cols else pd.DataFrame()
    if not numeric_profile.empty and "std" in numeric_profile.columns:
        numeric_profile = numeric_profile.sort_values("std", ascending=False)

    cat_cols = df_raw.select_dtypes(exclude=[np.number]).columns.tolist()
    categorical_profile = pd.DataFrame(
        {
            "n_unique": df_raw[cat_cols].nunique(dropna=False),
            "top": [
                df_raw[c].mode(dropna=False).iloc[0] if not df_raw[c].mode(dropna=False).empty else np.nan
                for c in cat_cols
            ],
            "top_freq": [
                df_raw[c].value_counts(dropna=False).iloc[0] if not df_raw[c].value_counts(dropna=False).empty else np.nan
                for c in cat_cols
            ],
        }
    ) if cat_cols else pd.DataFrame()

    missing_summary_path = results_dir / "missing_summary.csv"
    numeric_profile_path = results_dir / "numeric_profile.csv"
    categorical_profile_path = results_dir / "categorical_profile.csv"

    missing_summary.to_csv(missing_summary_path)
    numeric_profile.to_csv(numeric_profile_path)
    categorical_profile.to_csv(categorical_profile_path)

    print(f"Raw dataframe shape: {df_raw.shape}")
    print_saved_artifacts([missing_summary_path, numeric_profile_path, categorical_profile_path])


def main() -> None:
    parser = argparse.ArgumentParser(description="Notebook 01 as a reproducible script.")
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--input-path", default=None)
    parser.add_argument("--download-if-missing", action="store_true")
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--dataset-ref", default="manishabhatt22/marketing-campaign-performance-dataset")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    input_csv = resolve_input_path(repo_root, args.dataset, args.input_path)
    results_dir = repo_root / "results" / "initial_exploration"

    run_initial_exploration(input_csv, results_dir, args.download_if_missing, args.force_download, args.dataset_ref)


if __name__ == "__main__":
    main()

