"""Reproducible script for notebook 03: bivariate analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


DEFAULT_INPUT = "cleaned_marketing_dataset.csv"


def resolve_input_path(repo_root: Path, input_path: str | None, dataset_name: str) -> Path:
    if input_path:
        path = Path(input_path)
        return path if path.is_absolute() else (repo_root / path).resolve()
    return (repo_root / "datasets" / dataset_name).resolve()


def configure_plot_theme() -> None:
    plt.style.use("dark_background")
    sns.set_theme(style="darkgrid", context="notebook")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.facecolor"] = "#121212"
    plt.rcParams["figure.facecolor"] = "#121212"
    plt.rcParams["savefig.facecolor"] = "#121212"
    plt.rcParams["savefig.edgecolor"] = "#121212"
    plt.rcParams["axes.edgecolor"] = "#E0E0E0"
    plt.rcParams["axes.labelcolor"] = "#F5F5F5"
    plt.rcParams["xtick.color"] = "#E0E0E0"
    plt.rcParams["ytick.color"] = "#E0E0E0"
    plt.rcParams["text.color"] = "#F5F5F5"
    plt.rcParams["grid.color"] = "#3A3A3A"


def save_current_figure(output_path: Path) -> None:
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def print_saved_artifacts(artifacts: list[Path]) -> None:
    for artifact in artifacts:
        print(f"Saved: {artifact}")


def run_bivariate_analysis(input_csv: Path, results_dir: Path, alpha: float) -> None:
    if not input_csv.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {input_csv}")

    df = pd.read_csv(input_csv, parse_dates=["Date"])
    required_columns = [
        "Channel_Used",
        "ROI",
        "Target_Audience",
        "Conversion_Rate",
        "Acquisition_Cost",
        "Clicks",
        "Impressions",
        "Engagement_Score",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    results_dir.mkdir(parents=True, exist_ok=True)
    configure_plot_theme()

    plot_df = df[["Channel_Used", "ROI"]].dropna().copy()
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=plot_df, x="Channel_Used", y="ROI", palette="Set2")
    plt.title("ROI Distribution by Marketing Channel")
    plt.xlabel("Channel Used")
    plt.ylabel("ROI")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    roi_plot_path = results_dir / "roi_distribution_by_channel.png"
    save_current_figure(roi_plot_path)

    channel_roi_summary = (
        plot_df.groupby("Channel_Used")["ROI"]
        .agg(["count", "mean", "median", "std"])
        .sort_values(by="median", ascending=False)
    )

    audience_df = df[["Target_Audience", "Conversion_Rate"]].dropna().copy()
    audience_order = (
        audience_df.groupby("Target_Audience")["Conversion_Rate"].mean().sort_values(ascending=False).index
    )
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=audience_df,
        x="Target_Audience",
        y="Conversion_Rate",
        order=audience_order,
        estimator=np.mean,
        errorbar="sd",
        palette="Blues_d",
    )
    plt.title("Average Conversion Rate by Target Audience")
    plt.xlabel("Target Audience")
    plt.ylabel("Average Conversion Rate")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    audience_plot_path = results_dir / "avg_conversion_by_audience.png"
    save_current_figure(audience_plot_path)

    num_cols = [
        "Conversion_Rate",
        "Acquisition_Cost",
        "ROI",
        "Clicks",
        "Impressions",
        "Engagement_Score",
    ]
    corr_matrix = df[num_cols].corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        annot_kws={"size": 10},
    )
    plt.title("Correlation Heatmap: Marketing Performance Metrics")
    plt.tight_layout()
    corr_plot_path = results_dir / "correlation_heatmap.png"
    save_current_figure(corr_plot_path)

    google_roi = df.loc[df["Channel_Used"] == "Google Ads", "ROI"].dropna()
    youtube_roi = df.loc[df["Channel_Used"] == "YouTube", "ROI"].dropna()
    if len(google_roi) >= 2 and len(youtube_roi) >= 2:
        t_stat, p_value = stats.ttest_ind(google_roi, youtube_roi, equal_var=False)
    else:
        t_stat, p_value = np.nan, np.nan

    audience_conversion = (
        audience_df.groupby("Target_Audience")["Conversion_Rate"]
        .agg(["count", "mean", "std"])
        .sort_values("mean", ascending=False)
    )

    abs_corr_pairs = (
        corr_matrix.where(~np.eye(corr_matrix.shape[0], dtype=bool)).stack().abs().sort_values(ascending=False)
    )

    summary_rows: list[dict[str, object]] = []
    for channel, row in channel_roi_summary.iterrows():
        summary_rows.extend(
            [
                {"section": "channel_roi", "group": channel, "metric": "count", "value": row["count"]},
                {"section": "channel_roi", "group": channel, "metric": "mean", "value": row["mean"]},
                {"section": "channel_roi", "group": channel, "metric": "median", "value": row["median"]},
                {"section": "channel_roi", "group": channel, "metric": "std", "value": row["std"]},
            ]
        )

    for audience, row in audience_conversion.iterrows():
        summary_rows.extend(
            [
                {"section": "audience_conversion", "group": audience, "metric": "count", "value": row["count"]},
                {"section": "audience_conversion", "group": audience, "metric": "mean", "value": row["mean"]},
                {"section": "audience_conversion", "group": audience, "metric": "std", "value": row["std"]},
            ]
        )

    for pair, corr_value in abs_corr_pairs.head(6).items():
        summary_rows.append(
            {
                "section": "top_abs_correlation",
                "group": f"{pair[0]}__{pair[1]}",
                "metric": "abs_corr",
                "value": corr_value,
            }
        )

    summary_rows.extend(
        [
            {
                "section": "ttest_google_vs_youtube",
                "group": "google_vs_youtube",
                "metric": "google_n",
                "value": len(google_roi),
            },
            {
                "section": "ttest_google_vs_youtube",
                "group": "google_vs_youtube",
                "metric": "youtube_n",
                "value": len(youtube_roi),
            },
            {
                "section": "ttest_google_vs_youtube",
                "group": "google_vs_youtube",
                "metric": "t_stat",
                "value": t_stat,
            },
            {
                "section": "ttest_google_vs_youtube",
                "group": "google_vs_youtube",
                "metric": "p_value",
                "value": p_value,
            },
            {
                "section": "ttest_google_vs_youtube",
                "group": "google_vs_youtube",
                "metric": "alpha",
                "value": alpha,
            },
        ]
    )

    final_summary = pd.DataFrame(summary_rows)
    summary_csv_path = results_dir / "bivariate_final_summary.csv"
    final_summary.to_csv(summary_csv_path, index=False)

    print(f"Input file: {input_csv}")
    print_saved_artifacts([roi_plot_path, audience_plot_path, corr_plot_path, summary_csv_path])


def main() -> None:
    parser = argparse.ArgumentParser(description="Notebook 03 as a reproducible script.")
    parser.add_argument("--dataset", default=DEFAULT_INPUT, help="Cleaned CSV filename in datasets/.")
    parser.add_argument("--input-path", default=None, help="Optional absolute/relative cleaned CSV path.")
    parser.add_argument("--alpha", default=0.05, type=float, help="Significance threshold for t-test.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    input_csv = resolve_input_path(repo_root, args.input_path, args.dataset)
    results_dir = repo_root / "results" / "bivariate_analysis"

    run_bivariate_analysis(input_csv=input_csv, results_dir=results_dir, alpha=args.alpha)


if __name__ == "__main__":
    main()

