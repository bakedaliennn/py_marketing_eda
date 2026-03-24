# Diagnostic Report — Marketing Insight Lab

**Generated:** 2026-03-24  
**Branch:** `copilot/diagnostic-analysis-current-status`  
**Dataset:** Marketing Campaign Performance Dataset (Kaggle) — 200,000 campaign records

---

## 1. Project Context

Marketing Insight Lab follows two parallel tracks:

| Track | Goal |
|---|---|
| **Educational Realism** | Tune a synthetic dataset so it behaves like a plausible real-world marketing system for learning and portfolio use. |
| **Storytelling / BI** | Produce dashboard-ready outputs for Power BI and Tableau. |

The full pipeline moves raw data through cleaning, exploratory analysis, realism injection, validation, and re-analysis. Each stage has both a Jupyter notebook (for transparency) and a Python script (for fast reruns).

---

## 2. Completed Work Checklist

### Data Acquisition & Preparation

- [x] **01 — Initial Exploration** (`notebooks/01_initial_exploration.ipynb`, `scripts/initial_exploration.py`)
  - Raw dataset acquired and saved to `datasets/raw_marketing_dataset.csv` (200 k rows, 18 columns).
  - EDA and data quality checks completed.

- [x] **02 — Clean & Validate** (`notebooks/02_clean_and_validate.ipynb`, `scripts/clean_and_validate.py`)
  - Full cleaning transformations applied.
  - Cleaned dataset saved to `datasets/cleaned_marketing_dataset.csv`.

### Core Analysis (Cleaned Dataset)

- [x] **03 — Bivariate Analysis** (`notebooks/03_bivariate_analysis.ipynb`, `scripts/bivariate_analysis.py`)
  - Pairwise relationships, channel / audience performance, correlations, and hypothesis testing.
  - Outputs saved to `results/bivariate_analysis/`.
  - **Finding:** Channel ROI medians are nearly identical (~5.0 for all channels). All absolute correlations < 0.005. T-test Google vs YouTube: p = 0.48 (not significant). The dataset behaves too uniformly.

- [x] **04 — Multivariate Analysis** (`notebooks/04_multivariate_analysis.ipynb`, `scripts/multivariate_analysis.py`)
  - Linear regression, K-Means clustering (k = 3–6), PCA.
  - Outputs saved to `results/multivariate_analysis/`.
  - **Finding:** Regression R² ≈ 0 (−0.0002). Best silhouette score = 0.118 at k = 6. PCA PC1 + PC2 explain only 33.5 % of variance. The multivariate structure is effectively noise.

- [x] **05 — Actionable Recommendations** (`notebooks/05_actionable_recommendations.md`)
  - Ten-point transformation blueprint documented (channel profiles, audience interactions, seasonality, funnel mechanics, diminishing returns, lag effects, cluster archetypes, noise/outliers, categorical realism, realism scorecard).

### Realism Branch

- [x] **06 — Inject Realism** (`notebooks/06_inject_realism.ipynb`)
  - Channel-specific efficiency profiles applied.
  - Audience–campaign interaction effects applied.
  - Seasonality, funnel mechanics, cluster archetypes, and noise injected.
  - Realistic dataset saved to `datasets/realistic_marketing_dataset.csv`.

- [x] **07 — Realism Validation** (`notebooks/07_realism_validation.ipynb`)
  - Distribution checks, relationship checks, business rules, segment fidelity, and detectability tested.
  - Outputs saved to `results/realism_validation/`.
  - **Key scorecard metrics:**

| Metric | Value | Target / Interpretation |
|---|---|---|
| Numeric avg KS stat | 0.107 | Low–moderate distributional shift |
| Avg Wasserstein (cost/count) | 196 | Moderate numeric drift |
| Categorical avg JS divergence | 0.0 | Categorical distributions unchanged |
| Avg abs correlation delta | 0.061 | Correlations meaningfully shifted |
| Business rule violations | 0 / 4 rules | ✅ All constraints respected |
| Synthetic detectability AUC | **0.738** | ⚠️ Model can distinguish real vs synthetic fairly easily (target ≤ 0.65) |

- [x] **08 — Realism Analyses** (`notebooks/08_realism_analyses.ipynb`)
  - Full bivariate and multivariate analyses re-run on the realistic dataset.
  - Outputs saved to `results/realism_analyses/`.
  - **Improvement vs cleaned dataset:**

| Metric | Cleaned | Realistic | Change |
|---|---|---|---|
| Channel ROI spread (max − min median) | ~0.07 | ~2.76 | ✅ Large improvement |
| Google Ads median ROI | 5.01 | 5.72 | +14 % |
| YouTube median ROI | 4.97 | 2.96 | −40 % (lowest channel) |
| Top absolute correlation | 0.005 | **0.274** (ROI ↔ Acq. Cost) | ✅ Meaningful |
| Regression R² | −0.0002 | **0.281** | ✅ Substantial improvement |
| Best silhouette score | 0.118 | 0.136 | Modest improvement |
| Google vs YouTube t-test p-value | 0.484 | **~0** | ✅ Now highly significant |

---

## 3. Issues & Escalations

### 🔴 High Priority

| # | Issue | Evidence | Impact |
|---|---|---|---|
| H-1 | **Synthetic detectability too high** (AUC = 0.738) | `results/realism_validation/synthetic_detectability.csv` | A classifier can distinguish realistic from cleaned data too easily; the dataset is not yet "natural-looking". Target AUC ≤ 0.65. |
| H-2 | **Clicks–Impressions correlation is reversed** after realism injection | Correlation delta: Impressions↔Clicks = −0.178 (direction flipped) | Real marketing data always shows strong positive CTR dependency. This is a realism regression. |

### 🟡 Medium Priority

| # | Issue | Evidence | Impact |
|---|---|---|---|
| M-1 | **Cluster separation still weak** (silhouette = 0.136) | `results/realism_analyses/multivariate_analysis/multivariate_final_summary.csv` | The seven cluster archetypes defined in the blueprint are not yet clearly recoverable. Target silhouette ≥ 0.25. |
| M-2 | **Clicks distribution heavily shifted** (mean −38 %, std −24 %) | `results/realism_validation/numeric_fidelity_summary.csv` | Clicks dropped from median 550 to 313 — a large magnitude change that may break downstream funnel rate interpretations. |
| M-3 | **`results/realism_exploration/` directory does not exist** | README references `realism_exploration/realism_comparison_summary.csv` and `final_summary.csv` | README is partially inaccurate; outputs from notebook 06 are not persisted or are in a different location. |
| M-4 | **No `inject_realism.py` script** | `ls scripts/` — no script counterpart to notebook 06 | The script workflow is incomplete; fast reruns of the realism injection step are not possible. |

### 🟢 Low Priority / Observations

| # | Observation |
|---|---|
| L-1 | Categorical distributions are completely unchanged (JS divergence = 0) — this is expected since notebook 06 focuses on numeric realism, but adds no co-occurrence or frequency rebalancing from recommendation §9. |
| L-2 | `Duration` and `Campaign_ID` are identical between cleaned and realistic datasets (KS = 0, Wasserstein = 0) — no temporal or ID-level transformations applied. |
| L-3 | The BI / Storytelling branch has not started yet (no dashboard-ready output folder, no `.pbix` / Tableau packaged workbook). |
| L-4 | `scripts/__pycache__/` directory is tracked in git (should be excluded via `.gitignore`). |

---

## 4. Next Steps

### Immediate (address before resuming analysis)

1. **Fix the Clicks–Impressions correlation sign** (Issue H-2).
   - Re-examine the CTR / click generation logic in notebook 06 (`06_inject_realism.ipynb`).
   - Ensure `Clicks = Impressions × CTR` with CTR driven by channel and segment, not replacing raw Clicks with an independent draw.

2. **Reduce synthetic detectability** (Issue H-1).
   - Identify which features drive classifier separation (feature importance from the detectability model in notebook 07).
   - Smooth over-aggressive channel/audience multipliers to reduce bimodal distributions that are easy for a classifier to detect.
   - Re-run notebook 07 after changes to verify AUC drops toward 0.65.

3. **Add `.gitignore` entry for `__pycache__`** (Issue L-4).

### Short-term (complete the realism pipeline)

4. **Implement `scripts/inject_realism.py`** (Issue M-4) — a script-based counterpart to notebook 06 that reads `cleaned_marketing_dataset.csv` and writes `realistic_marketing_dataset.csv`.

5. **Improve cluster separation** (Issue M-1).
   - Implement the cluster-defining archetypes from recommendation §7 more explicitly: assign archetype labels during injection and verify that numeric features are drawn from archetype-specific distributions with sufficient between-archetype distance.
   - Target silhouette ≥ 0.25.

6. **Persist realism exploration outputs** (Issue M-3).
   - Ensure notebook 06 writes `results/realism_exploration/realism_comparison_summary.csv` and `final_summary.csv`, or update README to reflect where these outputs actually land.

7. **Add remaining realism transformations** from the blueprint not yet implemented:
   - §3 Seasonality, calendar effects, and trend.
   - §5 Diminishing returns and saturation curves.
   - §6 Lag and carryover effects.
   - §8 Controlled noise, outliers, and data quality artifacts.
   - §9 Categorical co-occurrence realism.

### Medium-term (start new tracks)

8. **Begin BI / Storytelling branch**:
   - Design wide-format output tables optimised for Power BI / Tableau.
   - Create a `results/dashboard_exports/` folder with pre-aggregated CSVs and time-series slices.
   - Document recommended chart types and KPI tiles per use case.

9. **Regression model improvements**:
   - Add nonlinear terms (log-spend, spend², interaction dummies) to close the gap between the current R² = 0.28 and a more realistic 0.45–0.55.
   - Consider adding a gradient-boosted model alongside linear regression in notebook 08 for comparison.

### Acceptance gates before closing the realism track

| Gate | Current | Target |
|---|---|---|
| Channel-pair ROI median differences > 5 % | ≥ 5 pairs ✅ | ≥ 3 pairs |
| Absolute correlations among core KPIs > 0.10 | 6 pairs ✅ | ≥ 4 pairs |
| Regression R² materially above 0 | 0.28 ✅ | > 0 |
| Silhouette score > baseline | 0.136 (marginal) | ≥ 0.25 |
| Synthetic detectability AUC | **0.738 ❌** | ≤ 0.65 |
| Zero business rule violations | 0 ✅ | 0 |
| Clicks–Impressions correlation positive | **Negative ❌** | > 0.30 |

---

## 5. Summary

The pipeline is structurally complete through all eight notebooks and the core analysis scripts. The realism injection phase produced meaningful improvements in channel differentiation, funnel correlations, and regression predictive power. However, **two hard blockers** (H-1, H-2) must be resolved before the realistic dataset can be considered trustworthy for portfolio or learning use: the synthetic data is still too detectable, and the Clicks–Impressions relationship was inadvertently inverted. Three medium-priority gaps (missing script, missing output directory, weak clustering) should be resolved in the same round of rework. Once those are fixed, the project is ready to begin the BI / Storytelling branch and optional advanced realism refinements.
