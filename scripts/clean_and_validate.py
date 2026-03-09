"""Reproducible script for notebook 02: clean and validate."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from clean_dataset import REQUIRED_COLUMNS, clean_dataset


DEFAULT_INPUT = "raw_marketing_dataset.csv"
DEFAULT_OUTPUT = "cleaned_marketing_dataset.csv"


def resolve_path(repo_root: Path, explicit_path: str | None, default_subpath: Path) -> Path:
    if explicit_path:
        path = Path(explicit_path)
        return path if path.is_absolute() else (repo_root / path).resolve()
    return (repo_root / default_subpath).resolve()


def print_saved_artifacts(artifacts: list[Path]) -> None:
    for artifact in artifacts:
        print(f"Saved: {artifact}")


def run_clean_and_validate(input_csv: Path, output_csv: Path, results_dir: Path) -> None:
    df_raw = pd.read_csv(input_csv)
    rows_before = len(df_raw)

    cleaned_df = clean_dataset(input_path=input_csv, output_path=output_csv)
    rows_after = len(cleaned_df)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in cleaned_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns after cleaning: {missing_columns}")

    results_dir.mkdir(parents=True, exist_ok=True)

    missing_summary = (
        pd.DataFrame(
            {
                "missing_count": cleaned_df.isna().sum(),
                "missing_pct": (cleaned_df.isna().mean() * 100).round(4),
            }
        )
        .sort_values(["missing_count", "missing_pct"], ascending=False)
    )
    numeric_profile = cleaned_df.describe(include=[np.number]).T.sort_values("std", ascending=False)

    missing_summary_path = results_dir / "missing_summary.csv"
    numeric_profile_path = results_dir / "numeric_profile.csv"
    missing_summary.to_csv(missing_summary_path)
    numeric_profile.to_csv(numeric_profile_path)

    validation_summary = pd.DataFrame(
        [
            {"metric": "rows_before", "value": rows_before},
            {"metric": "rows_after", "value": rows_after},
            {"metric": "duplicates_removed", "value": rows_before - rows_after},
            {"metric": "required_columns_count", "value": len(REQUIRED_COLUMNS)},
            {"metric": "missing_required_columns", "value": len(missing_columns)},
        ]
    )
    validation_summary_path = results_dir / "validation_summary.csv"
    validation_summary.to_csv(validation_summary_path, index=False)

    print(f"Input file: {input_csv}")
    print(f"Cleaned file: {output_csv}")
    print(f"Rows before: {rows_before}")
    print(f"Rows after: {rows_after}")
    print_saved_artifacts([missing_summary_path, numeric_profile_path, validation_summary_path])


def main() -> None:
    parser = argparse.ArgumentParser(description="Notebook 02 as a reproducible script.")
    parser.add_argument("--dataset", default=DEFAULT_INPUT)
    parser.add_argument("--input-path", default=None)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--output-path", default=None)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    input_csv = resolve_path(repo_root, args.input_path, Path("datasets") / args.dataset)
    output_csv = resolve_path(repo_root, args.output_path, Path("datasets") / args.output)
    results_dir = repo_root / "results" / "clean_and_validate"

    run_clean_and_validate(input_csv, output_csv, results_dir)


if __name__ == "__main__":
    main()

