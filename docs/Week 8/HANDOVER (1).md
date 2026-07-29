# Handover Document — CariSurg ED Triage Support Model

## 1. Project Summary
This repository contains the first modelling phase of an explainable AI-assisted triage support system for Emergency Department use. The model predicts Emergency Severity Index (ESI) — the 1–5 clinical acuity rating assigned at triage — from information available at the point of arrival: vital signs and chief-complaint flags. It is trained on the Yale EMMLC triage extract (55,121 de-identified adult ED encounters, Weeks 5–7 of this project), with demographic fields and outcome-only columns (`disposition`, `previousdispo`) deliberately excluded from the model inputs to avoid encoding bias and outcome leakage. The system is designed to support, not replace, clinician triage decisions — final acuity assignment remains the responsibility of the attending nurse or physician.

## 2. Final Model Decision
- **Model:** Logistic Regression (`max_iter=1000`, `random_state=42`, features imputed with median and standardised before training)
- **One-sentence why:** Logistic regression was the only model benchmarked across Weeks 6–7 (against a dummy baseline, decision tree, and random forest) that achieved non-zero recall on ESI Level 1 — the most critical patient class — while also being the fastest at inference and the easiest to explain to a clinician in plain language.
- Full reasoning: [`docs/decisions/2026-week-7-model-choice.md`](decisions/2026-week-7-model-choice.md)
- Full cost-benefit analysis: [`docs/Week7_Cost_Benefit_Memo.pdf`](Week7_Cost_Benefit_Memo.pdf)

## 3. How to Run

**Prerequisites:** Python 3.10+, git and pip already installed.

```bash
# 1. Clone the repository
git clone <repo-url>
cd carisurg-triage

# 2. Install dependencies (pinned versions — see requirements.txt)
pip install -r requirements.txt

# 3. Place the raw dataset (see "Where the Data Lives" below)
#    Expected path: data/yaleemmlc_admissionprediction_triage.csv

# 4. Run the sanity checks — should complete in under 2 seconds
pytest tests/ -v

# 5. Train the pinned model
python scripts/train.py --config config.yaml
```

Training on the full 55,121-row dataset takes well under a minute on a standard laptop (no GPU required). On success, `scripts/train.py` prints accuracy, precision, recall, F1, ESI-1 recall, training time, and inference time to the console, then saves the trained model to `models/logistic_regression.joblib` and a metrics snapshot to `docs/latest_run_metrics.json`.

## 4. Where the Data Lives
The raw dataset (`yaleemmlc_admissionprediction_triage.csv`, ~55MB, 55,121 de-identified adult ED encounters) is **not committed to this repository**. Large datasets are kept separate from code and documentation by convention, and this file — while de-identified — is still a sensitive clinical extract that shouldn't persist indefinitely in git history.

To run this pipeline, place the CSV at `data/yaleemmlc_admissionprediction_triage.csv` (this path is configurable via `config.yaml` → `data.raw_path`). The dataset used throughout this project was the Yale EMMLC triage extract provided for the CariSurg MedTech Pathways course. For a real Mercer deployment, this path would instead point to an approved, governed data extract from Mercer's own systems, following whatever data-access and consent process Martina Griffith's team requires — this repository does not currently implement any such access-control layer, and none should be assumed.

## 5. Known Limitations
- **Modest recall on the most critical class.** ESI Level 1 recall is approximately 0.40 in the most recent clean benchmark run — meaning roughly 6 in 10 of the most critical patients would still be missed if this model were used unmonitored today. This model is a defensible baseline, not a deployment-ready system.
- **Single-snapshot data, not a time-series.** The dataset captures one triage-time observation per patient, not sequential or repeated vitals over the course of a visit. This limits the model's ability to support "earlier identification of deteriorating patients" as described in the original problem statement — a genuine time-series extension would need different data.
- **Representativeness.** The training data is a single US academic-hospital sample. Case-mix, demographics, and access patterns may not transfer to a Caribbean ED context, and this has not yet been tested. Additionally, ESI distribution varies across race categories in ways that warrant ongoing fairness monitoring, not a one-time check (see Week 5 feasibility memo for detail).
