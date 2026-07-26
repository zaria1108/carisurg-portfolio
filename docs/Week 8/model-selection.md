# Model-Selection Results Table (Weeks 6–7)

This table is the audit trail behind the Week 7 model decision. Every model
trained across Weeks 6 and 7 is listed below, on the same train/test split
(`random_state=42`, 80/20 stratified on `esi`) so results are directly
comparable. 

**Status:** Draft — interim submission. Final submission will add any
additional tuning runs and cross-reference exact commit hashes.

| Model | Key Hyperparameters | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) | Recall (ESI 1) | Train Time (s) | Inference (ms/patient) |
|---|---|---|---|---|---|---|---|---|
| Dummy Baseline | `strategy="stratified"` | 0.370–0.389 | 0.200–0.201 | 0.200–0.201 | 0.200–0.201 | 0.000 | — | — |
| **Logistic Regression ⭐ (WINNER)** | `max_iter=1000`, median-imputed + scaled | 0.657–0.683 | 0.552–0.614 | 0.476–0.498 | 0.504–0.533 | **0.333–0.400** | ~11.2 | **~0.0035** |
| Decision Tree | `max_depth=5` | 0.553–0.571 | 0.242–0.270 | 0.249 | 0.222–0.224 | 0.000 | ~0.26 | ~0.0029 |
| Random Forest | `n_estimators=200`, `max_depth=10` | 0.587 | 0.333 | 0.267 | 0.245 | 0.000 | ~4.96 | ~0.101 |

*Note: Logistic regression's metrics show a small range across two separate clean re-runs in Week 6/7 (0.657 vs. 0.683 accuracy) due to a notebook restart between sessions — both runs are reported for transparency; the higher/most recent clean run is treated as authoritative.*

## Winner: Logistic Regression

**Marked as winner because:**
- Highest accuracy, precision, recall, and F1 of any model benchmarked
- **Only model with non-zero recall on ESI Level 1** — the single metric prioritised for clinical safety (missing a critical patient is far more dangerous than a false alarm)
- ~29x faster inference than Random Forest — relevant to Martina Griffith's compute-cost concern
- Explainable to a clinician in one sentence per prediction (one fixed coefficient per feature per class), unlike Random Forest's averaged, harder-to-explain-per-patient importances

## Known gaps in this draft (to close before final submission)
- [ ] Confirm which of the two logistic-regression accuracy figures (0.657 vs. 0.683) is reproducible from a single clean `Runtime → Restart → Run All`, and update this table with one authoritative number
- [ ] Link each row to the exact notebook/commit that produced it
- [ ] Add config.yaml hyperparameters verbatim once `scripts/train.py` is confirmed working end-to-end
