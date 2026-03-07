"""Reusable plotting helpers for marketing analysis notebooks."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Apply a consistent visual style across all notebook visualizations.
sns.set_theme(style="whitegrid")


def _get_results_dir() -> Path:
    """Return the repository results directory and ensure it exists."""
    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def plot_roi_distribution(df: pd.DataFrame) -> Path:
    """Plot ROI distribution with histogram and KDE overlay.

    Args:
        df: Input dataframe containing an ``ROI`` column.

    Returns:
        Path to the saved image file.

    Raises:
        KeyError: If ``ROI`` is not present in the dataframe.
    """
    if "ROI" not in df.columns:
        raise KeyError("Missing required column: 'ROI'")

    output_path = _get_results_dir() / "roi_distribution.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(
        data=df,
        x="ROI",
        kde=True,
        bins=30,
        color="#2f6f8f",
        edgecolor="white",
        alpha=0.85,
        ax=ax,
    )
    ax.set_title("ROI Distribution")
    ax.set_xlabel("ROI")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path


def plot_cost_vs_conversion(df: pd.DataFrame) -> Path:
    """Plot acquisition cost vs conversion rate by campaign type.

    Args:
        df: Input dataframe containing ``Acquisition_Cost``, ``Conversion_Rate``,
            and ``Campaign_Type`` columns.

    Returns:
        Path to the saved image file.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    required_cols = {"Acquisition_Cost", "Conversion_Rate", "Campaign_Type"}
    missing_cols = required_cols.difference(df.columns)
    if missing_cols:
        missing_list = sorted(missing_cols)
        raise KeyError(f"Missing required columns: {missing_list}")

    output_path = _get_results_dir() / "cost_vs_conversion.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="Acquisition_Cost",
        y="Conversion_Rate",
        hue="Campaign_Type",
        alpha=0.75,
        s=45,
        ax=ax,
    )
    ax.set_title("Acquisition Cost vs Conversion Rate by Campaign Type")
    ax.set_xlabel("Acquisition Cost")
    ax.set_ylabel("Conversion Rate")
    ax.legend(title="Campaign Type", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path
