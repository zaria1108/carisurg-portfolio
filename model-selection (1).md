# Model-Selection Results Table (Weeks 6–7)

This table is the audit trail behind the Week 7 model decision. Every model
trained across Weeks 6 and 7 is listed below, on the same train/test split
(`random_state=42`, 80/20 stratified on `esi`) so results are directly
comparable. Full reasoning for the final choice is in the
[Week 7 decision journal](decisions/2026-week-7-model-choice.md).

**Status:** Final. The gap flagged in the interim draft (two logistic
regression accuracy figures from separate notebook sessions) has been
resolved below — the authoritative numbers are the ones reported in the
[Week 7 Cost-Benefit Memo](Week7_Cost_Benefit_Memo.pdf), from the last
clean `Runtime → Restart → Run All` pass.

| Model | Key Hyperparameters | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) | Recall (ESI 1) | Train Time (s) | Inference (ms/patient) |
|---|---|---|---|---|---|---|---|---|
| Dummy Baseline | `strategy="stratified"` | 0.389 | 0.200 | 0.200 | 0.200 | 0.000 | — | — |
| **Logistic Regression ⭐ (WINNER — PINNED)** | `max_iter=1000`, median-imputed + scaled | **0.657** | 0.614 | 0.476 | 0.504 | **0.400** | 11.178 | **0.0035** |
| Decision Tree | `max_depth=5` | 0.571 | 0.242 | 0.249 | 0.222 | 0.000 | 0.259 | 0.0029 |
| Random Forest | `n_estimators=200`, `max_depth=10` | 0.587 | 0.333 | 0.267 | 0.245 | 0.000 | 4.962 | 0.101 |

**Note on the earlier draft:** the interim version of this table reported a
second logistic regression accuracy figure (0.683) from an earlier notebook
session with slightly different runtime state. That figure has been
superseded — 0.657 is the number reported in the final cost-benefit memo
and is treated as authoritative going forward. This discrepancy itself is
a useful reminder logged in the Week 7 conversation history: always
confirm results come from a single, clean, reproducible run before
reporting them as final.

## Winner: Logistic Regression

**Marked as winner because:**
- Highest accuracy, precision, and F1 of any real model benchmarked (dummy baseline excluded)
- **Only model with non-zero recall on ESI Level 1** — the metric prioritised for clinical safety, since missing a critical patient is far more dangerous than a false alarm
- ~29x faster inference than Random Forest (0.0035 ms vs. 0.101 ms per patient) — directly relevant to Martina Griffith's compute-cost concern
- Explainable to a clinician in one sentence per prediction (one fixed coefficient per feature per class), unlike Random Forest's harder-to-explain-per-patient averaged importances

Full reasoning: [`docs/decisions/2026-week-7-model-choice.md`](decisions/2026-week-7-model-choice.md)
Full cost-benefit analysis: [`docs/Week7_Cost_Benefit_Memo.pdf`](Week7_Cost_Benefit_Memo.pdf)

## Reproducing this table
```bash
python scripts/train.py --config config.yaml
```
`config.yaml` pins the winning model's exact hyperparameters. Running the
above will retrain logistic regression and print a fresh metrics snapshot
to the console and to `docs/latest_run_metrics.json`.
