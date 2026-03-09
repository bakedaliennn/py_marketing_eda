# Marketing EDA with Python

## Project Overview
This project analyzes marketing campaign performance data end-to-end with a notebook-first workflow and script-based automation.

Two development goals are reflected in the repository:
1. Notebook-first analysis: each stage of the pipeline is fully implemented and explained in notebooks.
2. Script automation: the same core tasks are also available through reusable Python scripts for quick execution.

## Dataset
Source: [Marketing Campaign Performance Dataset (Kaggle)](https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset)

The cleaned dataset includes 200,000 campaign records with fields such as:
- `Campaign_ID`, `Company`, `Campaign_Type`, `Target_Audience`
- `Duration`, `Channel_Used`, `Date`
- `Conversion_Rate`, `Acquisition_Cost`, `ROI`
- `Clicks`, `Impressions`, `Engagement_Score`
- `Customer_Segment`, `Location`, `Language`

## Repository Structure
- `dataset/`: legacy notebook raw-data path.
   - `marketing_campaign_dataset.csv`
- `datasets/`: script-first data path (raw, cleaned, and realism variants).
   - `marketing_campaign_dataset.csv`
   - `marketing_campaign_dataset_cleaned.csv`
   - `cleaned_marketing_campaign_dataset.csv`
   - `realistic_campaign_dataset.csv`
- `notebooks/`: full analytical pipeline notebooks.
   - `01_initial_exploration.ipynb`
   - `02_clean_and_validate.ipynb`
   - `03_bivariate_analysis.ipynb`
   - `04_multivariate_analysis.ipynb`
   - `05_actionable_recommendations.md`
   - `06_inject_realism.ipynb`
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
      - `avg_conversion_by_audience_dark.png`
      - `correlation_heatmap_dark.png`
      - `roi_distribution_by_channel_dark.png`
   - `multivariate_analysis/`
      - `multivariate_final_summary.csv`
      - `actual_vs_predicted_roi_dark.png`
      - `kmeans_clusters_pca_space_dark.png`
      - `pairplot_key_numeric_variables_dark.png`
      - `silhouette_scores_by_k_dark.png`

## Notebook Pipeline (Recommended for Learning and Review)
Run notebooks in this order:

1. `notebooks/01_initial_exploration.ipynb`
- Acquire raw dataset (reuse local file if already present).
- Perform raw-data EDA and quality checks.
- Saves/reuses `dataset/marketing_campaign_dataset.csv`.

2. `notebooks/02_clean_and_validate.ipynb`
- Apply full cleaning transformations directly in notebook cells.
- Validate cleaned schema and save `datasets/cleaned_marketing_campaign_dataset.csv`.

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
- Saves `datasets/realistic_campaign_dataset.csv`.

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
python scripts/initial_exploration.py --dataset marketing_campaign_dataset.csv
```

4. Run bivariate analysis:
```bash
python scripts/bivariate_analysis.py --dataset marketing_campaign_dataset_cleaned.csv
```

5. Run multivariate analysis:
```bash
python scripts/multivariate_analysis.py --dataset marketing_campaign_dataset_cleaned.csv
```

Note on cleaned file naming:
- Notebook `02_clean_and_validate.ipynb` currently writes `datasets/cleaned_marketing_campaign_dataset.csv`.
- Script workflow defaults to `datasets/marketing_campaign_dataset_cleaned.csv`.
- If you run analyses from notebook-cleaned output, pass `--dataset cleaned_marketing_campaign_dataset.csv` to scripts 03/04.

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
- Cleaned dataset saved to one of:
   - `datasets/marketing_campaign_dataset_cleaned.csv` (script default)
   - `datasets/cleaned_marketing_campaign_dataset.csv` (notebook 02 output)
- Realism-augmented dataset saved to `datasets/realistic_campaign_dataset.csv`
- Bivariate summary CSV saved to `results/bivariate_analysis/bivariate_final_summary.csv`
- Multivariate summary CSV saved to `results/multivariate_analysis/multivariate_final_summary.csv`
- Notebook-generated charts saved under `results/bivariate_analysis/` and `results/multivariate_analysis/`
- Script-generated summaries and charts saved under `results/initial_exploration/`, `results/clean_and_validate/`, `results/bivariate_analysis/`, and `results/multivariate_analysis/`

## License
This project is licensed under the MIT License. See `LICENSE` for details.
