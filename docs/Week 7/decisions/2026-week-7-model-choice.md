# Decision Journal: Model Choice for Phase 3

**Date:** Week 7, CariSurg MedTech Pathways
**Decision owner:** [Your Name]

## Context
- The Week 6 baseline (logistic regression) passed Dr. Reyes' review, and the ED Board asked whether a more sophisticated model would meaningfully improve triage-level prediction.
- Mercer IT Governance (Martina Griffith) raised compute and inference cost as a real constraint, not an afterthought — any model recommendation needs to account for deployment cost, not just accuracy.

## Alternatives Considered
- **Random Forest** (200 trees, max depth 10) — chosen as this week's complex-model candidate; a natural extension of the Week 6 decision tree, with built-in feature importances.
- **Gradient Boosting (XGBoost/LightGBM)** — considered but not implemented this week; likely more sensitive to tuning on this sparse, mostly-binary feature set, and would add another dependency to manage under IT Governance's constraints.
- **Small MLP (neural network)** — considered but rejected as disproportionate for a dataset of this size (~55k rows, ~200 mostly-sparse binary features) and would sacrifice interpretability entirely, which conflicts directly with Dr. Reyes' stated requirement.

## Decision
Keep the Week 6 logistic regression baseline as the recommended model for Phase 3; do not adopt the random forest.

## Reasoning
- Logistic regression outperformed the random forest on every accuracy-based metric, and was the only model of the four benchmarked to achieve any recall at all on ESI Level 1 (0.400 vs. 0.000).
- The random forest was roughly 29 times slower at inference per patient — a real, compounding cost in a real-time triage setting, and exactly the kind of hidden bill Martina Griffith was concerned about.
- Logistic regression's predictions can be explained to a clinician in one sentence, consistently, for every patient; the random forest's cannot, without additional tooling such as SHAP.

## Things I Do Not Yet Know
- Whether a random forest tuned specifically for class imbalance (e.g. `class_weight="balanced"`, different depth/estimator counts) could close the ESI Level 1 recall gap — this benchmark tested one reasonable configuration, not an exhaustive search.
- How stable these results are: the benchmark used a single train/test split, and the ESI Level 1 test set is very small (a handful of cases), so recall figures for the rarest class carry real sampling uncertainty that cross-validation would help quantify.
