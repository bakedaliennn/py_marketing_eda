# 05 Actionable Recommendations

## Why this file exists
The executive summaries in `03_bivariate_analysis.ipynb` and `04_multivariate_analysis.ipynb` point to the same issue: the cleaned dataset behaves too uniformly and does not express realistic marketing dynamics. ROI, conversion rates, and pairwise relationships are nearly flat, linear models explain little, and clusters are weakly separated.

This document provides actionable transformations to inject realism into the cleaned data while keeping it analytically usable.

## Key problems to correct
1. Channel performance is too similar (ROI distributions are almost identical).
2. Audience response is too similar (conversion rates by segment are nearly flat).
3. Correlations among core metrics are near zero, unlike real marketing systems.
4. Multivariate structure is weak (low predictive power, low cluster separability).
5. Time effects are underrepresented (seasonality, trend, campaign bursts, holidays).

## Transformation blueprint
Apply the transformations in this order so downstream effects compound in a realistic way.

### 1. Inject channel-specific efficiency profiles
Goal: make channels behave differently in cost and outcomes.

Actions:
- Assign a baseline efficiency multiplier per `Channel_Used` for both acquisition cost and conversion likelihood.
- Use plausible ranges instead of fixed constants, for example:
  - Search channel type: lower `Acquisition_Cost` median and higher conversion intent.
  - Video or display channel type: higher reach (`Impressions`) but lower immediate conversion.
  - Social channel type: higher engagement variance and mid-level conversion.
- Introduce channel-level variance so each channel has distinct spread, not only distinct means.

Implementation pattern:
- `Acquisition_Cost_new = Acquisition_Cost * channel_cost_multiplier * noise`
- `Conversion_Rate_new = clip(Conversion_Rate * channel_conv_multiplier + epsilon, 0, 1)`
- Recompute `ROI` after all upstream metric changes.

Validation checks:
- Median ROI by channel should be ranked but overlapping.
- Welch tests between at least two channel pairs should sometimes be significant and sometimes not.

### 2. Add audience-campaign interaction effects
Goal: make segments respond differently depending on campaign type and channel.

Actions:
- Create interaction multipliers for (`Target_Audience`, `Campaign_Type`, `Channel_Used`).
- Encode realistic compatibility patterns, for example:
  - Younger segments respond better to short-form social/video campaigns.
  - B2B-like audiences respond better to search and longer-duration informational campaigns.
- Keep effects probabilistic rather than deterministic to avoid perfect separability.

Implementation pattern:
- `segment_lift = interaction_lookup[(Target_Audience, Campaign_Type, Channel_Used)]`
- `Conversion_Rate_new = base_rate * segment_lift * random_jitter`

Validation checks:
- Mean conversion by audience should differ materially.
- In a regression with interaction terms, selected interactions should be non-zero and interpretable.

### 3. Add seasonality, calendar effects, and trend
Goal: represent temporal fluctuations common in marketing data.

Actions:
- Add weekly and monthly seasonality components.
- Add event windows (holiday peaks, promotional dips, post-promo decay).
- Add mild long-term drift (upward or downward trend) in cost and conversion.

Implementation pattern:
- Derive from `Date`: `day_of_week`, `month`, `is_holiday_window`, `quarter`.
- `season_factor = 1 + weekly_component + monthly_component + event_component + trend_component`
- Apply seasonality to `Impressions`, `Clicks`, and `Conversion_Rate` with different sensitivity per channel.

Validation checks:
- Time-series plots should show recurring patterns and non-flat variance.
- Correlation between time features and KPI shifts should be non-zero but not dominant.

### 4. Enforce realistic funnel mechanics
Goal: restore logical dependencies between impressions, clicks, conversions, cost, and ROI.

Actions:
- Generate or adjust metrics in causal order:
  1. `Impressions`
  2. `CTR` (from channel + audience + season)
  3. `Clicks = Impressions * CTR`
  4. `CVR` (from click quality + segment fit + campaign type)
  5. `Conversions = Clicks * CVR`
  6. `Spend` from clicks/impressions with channel-specific pricing
  7. `Revenue` from conversions and value-per-conversion
  8. `ROI = (Revenue - Spend) / Spend`
- Introduce bounded randomness at each stage.

Validation checks:
- `Clicks` should strongly correlate with `Impressions`.
- `Conversion_Rate` should correlate with `ROI` directionally.
- Funnel rates should remain in valid ranges.

### 5. Introduce diminishing returns and saturation
Goal: avoid unrealistic linear gain from endless spend.

Actions:
- Apply nonlinear response curves where incremental return drops at high spend/impression levels.
- Use channel-specific saturation thresholds.

Implementation pattern:
- Apply a Hill/log transform to conversion lift:
  - `effective_lift = max_lift * spend^alpha / (spend^alpha + half_sat^alpha)`
- For high `Impressions`, increase waste traffic probability (low-quality clicks).

Validation checks:
- Scatter `Spend` vs `ROI` should show curved or plateau behavior.
- Linear model fit should improve with nonlinear features (splines/log terms).

### 6. Create lag and carryover effects
Goal: include delayed impact often observed in brand and upper-funnel channels.

Actions:
- Add lagged exposure features by segment/channel (for example 7-day and 14-day rolling impressions/spend).
- Let part of current conversions depend on recent historical exposure.

Implementation pattern:
- Group by channel/segment and compute rolling windows on time-sorted data.
- `Conversion_Rate_t` partly depends on `lagged_impressions` and `lagged_clicks`.

Validation checks:
- Lagged features should have measurable explanatory value in multivariate models.
- Immediate-only models should underperform lag-aware models.

### 7. Add cluster-defining archetypes
Goal: produce meaningful segmentation structure for unsupervised learning.

Actions:
- Explicitly define 4-6 latent campaign archetypes (for example: high-reach low-ROI, efficient niche, expensive awareness, balanced performer).
- Sample campaigns from archetype-specific distributions for key numeric features.
- Keep overlap moderate so clusters are realistic but still recoverable.

Validation checks:
- Silhouette scores should improve from weak to moderate.
- Cluster profiles should show clear differences in at least 2-3 KPIs.

### 8. Add controlled noise, outliers, and data quality artifacts
Goal: mimic real system imperfections without breaking analysis.

Actions:
- Add heteroscedastic noise (variance increases with scale/spend).
- Inject a small fraction of anomalies:
  - unusually high spend with low return,
  - tracking glitches (temporary conversion spikes),
  - abrupt drops due to delivery issues.
- Add realistic missingness patterns (for example, missing engagement in specific channels or periods).

Validation checks:
- Outliers should be present but not dominate summaries.
- Missingness should be patterned, not purely uniform random.

### 9. Improve categorical realism
Goal: make category distributions and co-occurrences realistic.

Actions:
- Rebalance category frequencies to avoid near-uniform category counts.
- Add plausible dependencies:
  - some campaign types should appear more on specific channels,
  - some segments should be targeted more in certain seasons.

Validation checks:
- Crosstabs should show non-random structure (chi-square significance in selected pairs).
- No category should be excessively dominant unless intentionally modeled.

### 10. Build a realism scorecard and acceptance gates
Goal: verify that transformed data is realistic before analysis notebooks run.

Actions:
- Define acceptance thresholds for diagnostics:
  - minimum spread differences across channels,
  - non-trivial correlation magnitudes among funnel variables,
  - at least moderate explanatory power for multivariate models,
  - cluster separation above a baseline threshold,
  - detectable but not extreme seasonality.
- Save these diagnostics as a single CSV/Markdown audit report in `results/`.

Suggested acceptance examples (tune to your domain):
- At least 3 channel-pair ROI median differences greater than 5 percent.
- At least 4 absolute correlations greater than 0.10 among core numeric KPIs.
- Regression `R^2` positive and materially above zero.
- Silhouette score better than current baseline and stable across reruns.

## Practical execution plan
1. Create a transformation script (for example `scripts/inject_realism.py`) that reads `cleaned_marketing_dataset.csv` and writes `realistic_campaign_dataset.csv`.
2. Implement transformations in staged functions matching sections 1-9 above.
3. Seed randomness for reproducibility.
4. Run notebook 3 and notebook 4 on the realistic dataset.
5. Generate a before/after comparison report for:
   - channel ROI dispersion,
   - audience conversion differences,
   - correlation matrix strength,
   - regression diagnostics,
   - silhouette and cluster profile separation.

## Recommended feature additions (optional but high value)
- `Product_Category` or offer type to create differential conversion value.
- `Region` or market to induce geo-seasonal variation.
- `Device_Type` to model conversion efficiency differences.
- `Creative_Quality_Score` and `Landing_Page_Score` to explain conversion variance.
- `Competitor_Intensity` proxy for temporal performance pressure.

## Final note
Treat this as calibration, not random distortion. The objective is to generate data that behaves like a plausible marketing system: heterogeneous, partially predictable, temporally dynamic, and noisy enough to challenge both bivariate and multivariate analysis in a realistic way.

