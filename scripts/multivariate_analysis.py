"""Reproducible script for notebook 04: multivariate analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DEFAULT_INPUT = "marketing_campaign_dataset_cleaned.csv"


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


def run_multivariate_analysis(input_csv: Path, results_dir: Path) -> None:
    if not input_csv.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {input_csv}")

    df = pd.read_csv(input_csv, parse_dates=["Date"])
    results_dir.mkdir(parents=True, exist_ok=True)
    configure_plot_theme()

    target = "ROI"
    numeric_features = [
        "Conversion_Rate",
        "Acquisition_Cost",
        "Clicks",
        "Impressions",
        "Engagement_Score",
        "Duration",
    ]
    categorical_features = ["Channel_Used", "Campaign_Type", "Target_Audience", "Customer_Segment"]

    required = [target, *numeric_features, *categorical_features]
    missing_required = [c for c in required if c not in df.columns]
    if missing_required:
        raise ValueError(f"Missing required columns for multivariate analysis: {missing_required}")

    model_df = df[required].dropna().reset_index(drop=True)
    if len(model_df) < 10:
        raise ValueError("Not enough complete rows after dropna to run multivariate analysis.")

    X_num = model_df[numeric_features].copy()
    X_cat = pd.get_dummies(model_df[categorical_features], drop_first=True)
    X = pd.concat([X_num, X_cat], axis=1)
    y = model_df[target].astype(float)

    pair_cols = ["ROI", "Conversion_Rate", "Acquisition_Cost", "Clicks", "Impressions", "Engagement_Score"]
    pair_df = model_df[pair_cols].sample(min(3000, len(model_df)), random_state=42)
    pair_grid = sns.pairplot(pair_df, corner=True, diag_kind="hist", plot_kws={"alpha": 0.3, "s": 12})
    pair_grid.fig.suptitle("Pairplot of Key Numeric Variables (Sample)", y=1.02)
    pair_grid.fig.tight_layout()
    pairplot_path = results_dir / "pairplot_key_numeric_variables_dark.png"
    pair_grid.fig.savefig(pairplot_path, dpi=300, bbox_inches="tight")
    plt.close(pair_grid.fig)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    coef_df = pd.DataFrame({"feature": X.columns, "coefficient": reg.coef_})
    coef_df["abs_coefficient"] = coef_df["coefficient"].abs()
    coef_df = coef_df.sort_values("abs_coefficient", ascending=False)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.4)
    min_v = min(y_test.min(), y_pred.min())
    max_v = max(y_test.max(), y_pred.max())
    plt.plot([min_v, max_v], [min_v, max_v], color="red", linestyle="--", linewidth=1.5)
    plt.title("Actual vs Predicted ROI (Multivariate Regression)")
    plt.xlabel("Actual ROI")
    plt.ylabel("Predicted ROI")
    plt.tight_layout()
    actual_vs_pred_path = results_dir / "actual_vs_predicted_roi_dark.png"
    plt.savefig(actual_vs_pred_path, dpi=300, bbox_inches="tight")
    plt.close()

    cluster_features = ["Conversion_Rate", "Acquisition_Cost", "ROI", "Clicks", "Impressions", "Engagement_Score"]
    cluster_df = model_df[cluster_features].dropna().copy()
    scaler = StandardScaler()
    X_cluster_scaled = scaler.fit_transform(cluster_df)

    candidate_k = [k for k in [3, 4, 5, 6] if k < len(cluster_df)]
    if not candidate_k:
        candidate_k = [2] if len(cluster_df) > 2 else []
    if not candidate_k:
        raise ValueError("Not enough rows to run KMeans clustering.")

    silhouette_sample_size = min(20000, len(cluster_df))
    scores: list[tuple[int, float]] = []
    for k in candidate_k:
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(X_cluster_scaled)
        score = silhouette_score(
            X_cluster_scaled,
            labels,
            sample_size=silhouette_sample_size,
            random_state=42,
        )
        scores.append((k, score))

    silhouette_df = pd.DataFrame(scores, columns=["k", "silhouette_score"]).sort_values(
        "silhouette_score", ascending=False
    )
    best_k = int(silhouette_df.iloc[0]["k"])

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=silhouette_df.sort_values("k"), x="k", y="silhouette_score", marker="o")
    plt.title("Silhouette Score by Number of Clusters (K)")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    silhouette_plot_path = results_dir / "silhouette_scores_by_k_dark.png"
    plt.savefig(silhouette_plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    kmeans = KMeans(n_clusters=best_k, n_init=20, random_state=42)
    cluster_df["cluster"] = kmeans.fit_predict(X_cluster_scaled)

    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(X_cluster_scaled)
    pca_plot_df = pd.DataFrame(
        {
            "PC1": pcs[:, 0],
            "PC2": pcs[:, 1],
            "cluster": cluster_df["cluster"].values,
        }
    )

    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=pca_plot_df, x="PC1", y="PC2", hue="cluster", palette="tab10", alpha=0.65)
    plt.title("K-Means Clusters Projected onto 2D PCA Space")
    plt.tight_layout()
    pca_clusters_path = results_dir / "kmeans_clusters_pca_space_dark.png"
    plt.savefig(pca_clusters_path, dpi=300, bbox_inches="tight")
    plt.close()

    explained = pca.explained_variance_ratio_
    cluster_counts = cluster_df["cluster"].value_counts().sort_index()
    cluster_means = cluster_df.groupby("cluster")[cluster_features].mean()

    summary_rows: list[dict[str, object]] = []
    summary_rows.extend(
        [
            {"section": "regression_metrics", "group": "linear_regression", "metric": "r2", "value": r2},
            {"section": "regression_metrics", "group": "linear_regression", "metric": "mae", "value": mae},
            {
                "section": "regression_metrics",
                "group": "linear_regression",
                "metric": "rmse",
                "value": rmse,
            },
            {
                "section": "regression_metrics",
                "group": "linear_regression",
                "metric": "train_rows",
                "value": len(X_train),
            },
            {
                "section": "regression_metrics",
                "group": "linear_regression",
                "metric": "test_rows",
                "value": len(X_test),
            },
        ]
    )

    for _, row in coef_df.head(15).iterrows():
        summary_rows.append(
            {
                "section": "top_coefficients",
                "group": row["feature"],
                "metric": "coefficient",
                "value": row["coefficient"],
            }
        )

    for _, row in silhouette_df.sort_values("k").iterrows():
        summary_rows.append(
            {
                "section": "silhouette_scores",
                "group": f"k_{int(row['k'])}",
                "metric": "silhouette_score",
                "value": row["silhouette_score"],
            }
        )
    summary_rows.append(
        {"section": "silhouette_scores", "group": "model_selection", "metric": "best_k", "value": best_k}
    )

    for cluster_label, count in cluster_counts.items():
        summary_rows.append(
            {
                "section": "cluster_sizes",
                "group": f"cluster_{int(cluster_label)}",
                "metric": "count",
                "value": count,
            }
        )

    for cluster_label, row in cluster_means.iterrows():
        for feature in cluster_features:
            summary_rows.append(
                {
                    "section": "cluster_feature_means",
                    "group": f"cluster_{int(cluster_label)}",
                    "metric": feature,
                    "value": row[feature],
                }
            )

    summary_rows.extend(
        [
            {"section": "pca", "group": "variance", "metric": "pc1_explained_ratio", "value": explained[0]},
            {"section": "pca", "group": "variance", "metric": "pc2_explained_ratio", "value": explained[1]},
            {
                "section": "pca",
                "group": "variance",
                "metric": "pc1_pc2_total_ratio",
                "value": explained[0] + explained[1],
            },
        ]
    )

    multivariate_summary = pd.DataFrame(summary_rows)
    multivariate_summary_csv_path = results_dir / "multivariate_final_summary.csv"
    multivariate_summary.to_csv(multivariate_summary_csv_path, index=False)

    print(f"Input file: {input_csv}")
    print(f"Rows used for modeling: {len(model_df)}")
    print(f"R^2: {r2:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")
    print(f"Saved: {pairplot_path}")
    print(f"Saved: {actual_vs_pred_path}")
    print(f"Saved: {silhouette_plot_path}")
    print(f"Saved: {pca_clusters_path}")
    print(f"Saved summary CSV: {multivariate_summary_csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Notebook 04 as a reproducible script.")
    parser.add_argument("--dataset", default=DEFAULT_INPUT, help="Cleaned CSV filename in datasets/.")
    parser.add_argument("--input-path", default=None, help="Optional absolute/relative cleaned CSV path.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    input_csv = resolve_input_path(repo_root, args.input_path, args.dataset)
    results_dir = repo_root / "results" / "multivariate_analysis" / input_csv.stem

    run_multivariate_analysis(input_csv=input_csv, results_dir=results_dir)


if __name__ == "__main__":
    main()
