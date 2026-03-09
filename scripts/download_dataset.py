"""Download a raw marketing dataset from Kaggle into the local datasets folder."""

from __future__ import annotations

import shutil
from pathlib import Path


DEFAULT_DATASET_REF = "manishabhatt22/marketing-campaign-performance-dataset"
DEFAULT_CSV_NAME = "marketing_campaign_dataset.csv"


def download_kaggle_dataset(
    dataset_ref: str = DEFAULT_DATASET_REF,
    csv_name: str = DEFAULT_CSV_NAME,
) -> Path:
    """Download a Kaggle dataset and copy one CSV into ``datasets``.

    Args:
        dataset_ref: Kaggle dataset identifier in ``owner/dataset`` format.
        csv_name: Expected CSV filename inside downloaded files.

    Returns:
        Absolute path to the copied CSV in ``datasets``.
    """
    try:
        import kagglehub
    except ImportError as exc:
        raise RuntimeError("kagglehub is required. Install it with: pip install kagglehub") from exc

    try:
        downloaded_dir = Path(kagglehub.dataset_download(dataset_ref)).resolve()
    except Exception as exc:
        raise RuntimeError(f"Failed to download dataset '{dataset_ref}': {exc}") from exc

    source_csv = downloaded_dir / csv_name
    if not source_csv.exists():
        csv_candidates = sorted(downloaded_dir.rglob("*.csv"))
        if not csv_candidates:
            raise FileNotFoundError(f"No CSV files found in downloaded path: {downloaded_dir}")
        source_csv = csv_candidates[0]

    repo_root = Path(__file__).resolve().parent.parent
    dataset_dir = repo_root / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)

    destination_csv = dataset_dir / csv_name
    shutil.copy2(source_csv, destination_csv)
    return destination_csv


if __name__ == "__main__":
    output_path = download_kaggle_dataset()
    print(f"Raw dataset saved to: {output_path}")
