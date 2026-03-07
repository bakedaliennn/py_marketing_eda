# Marketing EDA with Python

## Project Overview
This project analyzes marketing campaign performance data end-to-end using a notebook-first workflow and script-based automation.

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
- `dataset/`: raw and cleaned CSV files.
   - `marketing_campaign_dataset.csv`
   - `marketing_campaign_dataset_cleaned.csv`
- `notebooks/`: full analytical pipeline notebooks.
   - `01_initial_exploration.ipynb`
   - `02_clean_and_validate.ipynb`
   - `03_bivariate_analysis.ipynb`
   - `04_multivariate_analysis.ipynb`
- `scripts/`: reusable automation modules.
   - `kaggle_import.py`
   - `data_cleaner.py`
   - `visualize.py`
- `results/`: exported charts and outputs.

## Notebook Pipeline (Recommended for Learning and Review)
Run notebooks in this order:

1. `notebooks/01_initial_exploration.ipynb`
- Acquire raw dataset (reuse local file if already present).
- Perform raw-data EDA and quality checks.

2. `notebooks/02_clean_and_validate.ipynb`
- Apply full cleaning transformations directly in notebook cells.
- Validate cleaned schema and save `dataset/marketing_campaign_dataset_cleaned.csv`.

3. `notebooks/03_bivariate_analysis.ipynb`
- Analyze pairwise relationships, channel and audience performance, correlations, and hypothesis testing.

4. `notebooks/04_multivariate_analysis.ipynb`
- Perform multivariate modeling and segmentation (regression, clustering, PCA).

## Script Workflow (Recommended for Fast Reproducible Runs)
Use scripts when you want faster execution outside notebooks.

1. Download raw data:
```bash
python scripts/kaggle_import.py
```

2. Clean dataset:
```bash
python scripts/data_cleaner.py
```

3. Use plotting helpers from `scripts/visualize.py` in your own driver script or notebook.

## Setup
1. Clone repository:
```bash
git clone <repository-url>
cd py_marketing_eda
```

2. Create and activate a Python environment.

3. Install dependencies (minimum):
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy kagglehub
```

4. Run either the notebook pipeline or script workflow.

## Outputs
- Cleaned dataset saved to `dataset/marketing_campaign_dataset_cleaned.csv`
- Optional figures saved to `results/` (when using visualization helpers/export steps)

## License
This project is licensed under the MIT License. See `LICENSE` for details.
