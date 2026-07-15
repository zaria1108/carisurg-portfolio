# Week 6 – Baseline Model Development & Clinical Communication

## Objective
To build and evaluate a defensible baseline classifier for ED triage level prediction, select and justify a primary performance metric appropriate for a clinically imbalanced, high-stakes classification task, and communicate the results honestly to a non-technical clinical reviewer.

## Activities Completed
- Selected features (vitals + chief-complaint flags), explicitly excluding demographic fields and leakage columns (`disposition`, `previousdispo`) from model inputs
- Split the dataset 80/20, stratified on `esi`, with a committed random seed (`random_state=42`) for reproducibility
- Built a stratified `DummyClassifier` as the floor baseline every real model must beat
- Trained and evaluated a **Logistic Regression** classifier (median-imputed, scaled features)
- Trained and evaluated a **Decision Tree** classifier (`max_depth=5`, unscaled features), justified by the trade-off between explainability and overfitting risk
- Computed accuracy, per-class precision/recall/F1, macro F1, and weighted F1 for all three models
- Generated and saved confusion matrices for all three models
- Selected **recall for ESI Level 1** as the primary clinical metric and wrote a one-paragraph justification centred on the asymmetric cost of under-triage vs. over-triage
- Documented the most concerning failure mode: the decision tree achieves 0.000 recall on ESI Level 1, missing every critical patient in the test set, despite 0.571 overall accuracy
- Wrote a three-page baseline report (introduction, methods, results, metric justification, failure-mode reflection, conclusion)
- Scripted a one-minute clinical explainer video for Dr. Reyes, translating the recall finding into plain patient-outcome language without using the words "recall," "precision," or "F1"

## Model Comparison

| Model | Accuracy | Macro F1 | Weighted F1 | Recall (ESI 1) |
|---|---|---|---|---|
| Dummy Baseline | 0.389 | 0.200 | 0.387 | 0.000 |
| Logistic Regression | 0.657 | 0.504 | 0.653 | 0.333 |
| Decision Tree | 0.571 | 0.222 | 0.480 | 0.000 |

## Primary Metric Justification
Overall accuracy is a poor guide on this severely imbalanced target: a model can score well by predicting the common mid-acuity classes correctly while ignoring the rare, critical ESI Level 1 class entirely. Recall for ESI Level 1 was chosen as the primary metric because missing a critically ill patient (under-triage) carries far greater clinical risk than a false alarm (over-triage) — the latter costs a few minutes of clinician review, the former risks delayed resuscitation.

## Failure Mode
The decision tree's 0.000 recall on ESI Level 1 — confirmed further by scikit-learn's precision warnings showing the tree never predicts ESI Level 1, 4, or 5 at all — is the clearest evidence that neither baseline is yet fit for clinical deployment, and that future work must directly address class imbalance rather than pursue model complexity for its own sake.

## Deliverables
- [x] Baseline notebook with all three models (`notebooks/week6_baseline_models.ipynb`)
- [x] Confusion matrices for all three models (`docs/confusion_matrix_*.png`)
- [x] Model comparison table
- [x] Three-page baseline report (`docs/Week6_Baseline_Report.pdf`)
- [x] Primary metric justification and macro-vs-weighted F1 explanation
- [x] Failure-mode reflection
- [x] One-minute Loom clinical explainer script
- [ ] Loom video recorded and posted to Discord

## Reflection
This week made the gap between a working model and a *safe* model impossible to ignore. Both baselines clear a reasonable accuracy bar, but the metric that actually matters — catching the sickest patients — exposed the decision tree as unfit for purpose despite looking competitive on paper. Writing the explainer script was its own exercise in honesty: translating "recall = 0.333" into "we'd catch about 3 in 10 of the most critical patients" made the stakes concrete in a way the number alone did not, and reinforced why Dr. Reyes's scepticism toward unexplained metrics is the right default, not an obstacle to work around.
