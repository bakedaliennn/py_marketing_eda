# Marketing Insight Lab

## Project Overview
Marketing Insight Lab analyzes marketing campaign performance end-to-end with a notebook-first workflow and script-based automation.

Two core goals drive this repository:
1. Educational realism branch: fine-tune synthetic realism so the dataset can be reused for learning and portfolio projects.
2. Storytelling branch: prepare dashboard-ready outputs for BI tools such as Power BI and Tableau.

Each stage is implemented in notebooks for transparency and reproducibility, with matching Python scripts for faster reruns.

## Dataset
Source: [Marketing Campaign Performance Dataset (Kaggle)](https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset)

The cleaned dataset includes 200,000 campaign records with fields such as:
- `Campaign_ID`, `Company`, `Campaign_Type`, `Target_Audience`
- `Duration`, `Channel_Used`, `Date`
- `Conversion_Rate`, `Acquisition_Cost`, `ROI`
- `Clicks`, `Impressions`, `Engagement_Score`
- `Customer_Segment`, `Location`, `Language`

## Repository Structure
- `datasets/`: script-first data path (raw, cleaned, and realism variants).
   - `raw_marketing_dataset.csv`
   - `cleaned_marketing_dataset.csv`
   - `realistic_marketing_dataset.csv`
- `notebooks/`: full analytical pipeline notebooks.
   - `01_initial_exploration.ipynb`
   - `02_clean_and_validate.ipynb`
   - `03_bivariate_analysis.ipynb`
   - `04_multivariate_analysis.ipynb`
   - `05_actionable_recommendations.md`
   - `06_inject_realism.ipynb`
   - `07_realism_validation.ipynb`
   - `08_realism_analyses.ipynb`
- `scripts/`: reusable automation modules.
   - `download_dataset.py`
   - `clean_dataset.py`
   - `initial_exploration.py`
   - `clean_and_validate.py`
   - `bivariate_analysis.py`
   - `multivariate_analysis.py`
- `results/`: exported charts and outputs.
   - `bivariate_analysis/`
      - `bivariate_final_summary.csv`
      - `avg_conversion_by_audience.png`
      - `correlation_heatmap.png`
      - `roi_distribution_by_channel.png`
   - `multivariate_analysis/`
      - `multivariate_final_summary.csv`
      - `actual_vs_predicted_roi.png`
      - `kmeans_clusters_pca_space.png`
      - `pairplot_key_numeric_variables.png`
      - `silhouette_scores_by_k.png`
   - `realism_exploration/`
      - `realism_comparison_summary.csv`
      - `final_summary.csv`
   - `realism_validation/`
      - `realism_validation_overview.csv`
      - `synthetic_detectability.csv`
      - `numeric_fidelity_summary.csv`
      - `categorical_fidelity_summary.csv`
   - `realism_analyses/`
      - `bivariate_analysis/bivariate_final_summary.csv`
      - `multivariate_analysis/multivariate_final_summary.csv`

## Notebook Pipeline (Recommended for Learning and Review)
Run notebooks in this order:

1. `notebooks/01_initial_exploration.ipynb`
- Acquire raw dataset (reuse local file if already present).
- Perform raw-data EDA and quality checks.
- Saves/reuses `datasets/raw_marketing_dataset.csv`.

2. `notebooks/02_clean_and_validate.ipynb`
- Apply full cleaning transformations directly in notebook cells.
- Validate cleaned schema and save `datasets/cleaned_marketing_dataset.csv`.

3. `notebooks/03_bivariate_analysis.ipynb`
- Analyze pairwise relationships, channel and audience performance, correlations, and hypothesis testing.
- Export final summary and charts to `results/bivariate_analysis/`.

4. `notebooks/04_multivariate_analysis.ipynb`
- Perform multivariate modeling and segmentation (regression, clustering, PCA).
- Export final summary and charts to `results/multivariate_analysis/`.

5. `notebooks/05_actionable_recommendations.md`
- Summarizes insights and recommendations derived from the analysis outputs.

6. `notebooks/06_inject_realism.ipynb`
- Applies realism transformations (channel effects, seasonality, interaction effects, controlled artifacts).
- Saves `datasets/realistic_marketing_dataset.csv`.
- Saves `results/realism_exploration/realism_comparison_summary.csv`.

7. `notebooks/07_realism_validation.ipynb`
- Validates realism quality versus cleaned baseline using distribution checks, relationship checks, business rules, segment fidelity, and detectability.
- Saves validation scorecards under `results/realism_validation/`.

8. `notebooks/08_realism_analyses.ipynb`
- Runs full bivariate + multivariate analyses on the realism-injected dataset.
- Saves analysis outputs under `results/realism_analyses/`.

## Script Workflow (Recommended for Fast Reproducible Runs)
Use scripts when you want faster execution outside notebooks.

1. Download raw data:
```bash
python scripts/download_dataset.py
```

2. Clean dataset:
```bash
python scripts/clean_and_validate.py
```

3. Run initial exploration:
```bash
python scripts/initial_exploration.py --dataset raw_marketing_dataset.csv
```

4. Run bivariate analysis:
```bash
python scripts/bivariate_analysis.py --dataset cleaned_marketing_dataset.csv
```

5. Run multivariate analysis:
```bash
python scripts/multivariate_analysis.py --dataset cleaned_marketing_dataset.csv
```

Note on cleaned file naming:
- Notebook `02_clean_and_validate.ipynb` currently writes `datasets/cleaned_marketing_dataset.csv`.
- Script workflow defaults to `datasets/cleaned_marketing_dataset.csv`.
- Use `--dataset cleaned_marketing_dataset.csv` for scripts 03/04.

## Setup
1. Clone repository:
```bash
git clone <repository-url>
cd py_marketing_eda
```

2. Create and activate a Python environment.

3. If you plan to run Kaggle import, configure your Kaggle credentials first (for example `kaggle.json` in the standard Kaggle config location).

4. Install dependencies (minimum):
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy kagglehub
```

5. Run either the notebook pipeline or script workflow.

## Outputs
- Cleaned dataset saved to `datasets/cleaned_marketing_dataset.csv`
- Realism-augmented dataset saved to `datasets/realistic_marketing_dataset.csv`
- Realism comparison summary saved to `results/realism_exploration/realism_comparison_summary.csv`
- Realism exploration final summary saved to `results/realism_exploration/final_summary.csv`
- Realism validation scorecard saved to `results/realism_validation/realism_validation_overview.csv`
- Synthetic detectability summary saved to `results/realism_validation/synthetic_detectability.csv`
- Bivariate summary CSV saved to `results/bivariate_analysis/bivariate_final_summary.csv`
- Multivariate summary CSV saved to `results/multivariate_analysis/multivariate_final_summary.csv`
- Realism-branch analysis summaries saved under `results/realism_analyses/bivariate_analysis/` and `results/realism_analyses/multivariate_analysis/`
- Notebook-generated charts saved under `results/bivariate_analysis/`, `results/multivariate_analysis/`, `results/realism_exploration/`, `results/realism_validation/`, and `results/realism_analyses/`
- Script-generated summaries and charts saved under `results/initial_exploration/`, `results/clean_and_validate/`, `results/bivariate_analysis/`, and `results/multivariate_analysis/`

## License
This project is licensed under the MIT License. See `LICENSE` for details.


