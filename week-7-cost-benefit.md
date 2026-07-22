# Week 7 Cost-Benefit Memo: Is a More Complex Model Worth It?

**To:** Dr. De Fretias, ED Board, Martina Griffith (Clinical IT Lead)
**From:** [Your Name]
**Re:** Random Forest vs. Logistic Regression Baseline — Recommendation for Phase 3

---

## Verdict

**Do not adopt the random forest. The Week 6 logistic regression baseline remains the recommended model for Phase 3** — it is more accurate, faster at inference, and considerably easier to explain to a clinician, and the added complexity of a random forest bought no improvement whatsoever on the one metric that matters most: catching the sickest patients.

## Dataset and Methods Recap

This benchmark reuses the Week 5–6 Yale EMMLC triage extract (55,121 adult ED encounters) and the exact same 80/20 stratified train/test split (`random_state=42`) established in Week 6, so results are directly comparable. Four models were evaluated: a stratified dummy baseline, the Week 6 logistic regression and decision tree baselines, and a new Random Forest classifier (200 trees, max depth 10) as this week's complex-model candidate. All models were trained and evaluated on the same feature set — vital signs and chief-complaint flags, with demographic fields and outcome-leakage columns (`disposition`, `previousdispo`) excluded throughout.

## Benchmark Table

| Model | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) | Train Time (s) | Inference (ms/patient) | Recall (ESI 1) |
|---|---|---|---|---|---|---|---|
| Dummy Baseline | 0.370 | 0.201 | 0.201 | 0.201 | — | — | 0.000 |
| **Logistic Regression** | **0.683** | **0.614** | **0.498** | **0.533** | 11.178 | **0.0035** | **0.400** |
| Decision Tree | 0.553 | 0.242 | 0.249 | 0.224 | 0.259 | 0.0029 | 0.000 |
| Random Forest | 0.587 | 0.333 | 0.267 | 0.245 | 4.962 | 0.101 | 0.000 |

Logistic regression leads on every accuracy-based metric and, critically, is the only model to catch any ESI Level 1 patients at all (recall 0.400, versus 0.000 for both the decision tree and the random forest).

## Interpretability

![Feature importance comparison](interpretability_comparison.png)

*Figure 1: Random Forest feature importances (left) vs. Logistic Regression coefficient magnitudes (right). Both models agree that `cc_abdominalpain`, `cc_chestpain`, and `triage_vital_o2_device` are strong signals.*

**Logistic regression: explainable in under a minute.** Each feature carries one fixed, signed coefficient per class, so a single prediction can be explained in one sentence — "this patient was flagged as higher acuity mainly due to abdominal pain and altered mental status." The explanation method is identical for every patient.

**Random forest: not explainable in under a minute.** Feature importances describe average behaviour across all 55,121 patients, not the reasoning behind any one specific prediction, which is instead the averaged vote of 200 individual trees. Explaining a single prediction properly would require a tool such as SHAP — a legitimate further analysis step, but not a bedside conversation.

## Three Arguments For the Recommended Choice (Logistic Regression)

1. **It is the only model that catches any critical patients.** A 0.400 recall on ESI Level 1 is still far from adequate, but it is meaningfully better than the 0.000 achieved by both the decision tree and the random forest — the two models notionally more sophisticated than it.
2. **It is roughly 29 times faster at inference** than the random forest (0.0035 ms vs. 0.101 ms per patient). In a real-time triage setting, this difference compounds across every patient, every shift, indefinitely.
3. **It is transparent by construction.** Every prediction can be explained to a clinician in one sentence, with the same reasoning applied consistently to every patient — a requirement Dr. Reyes has stated explicitly, not a nice-to-have.

## Three Arguments Against the Recommended Choice

1. **Its overall recall (macro) is still modest (0.498)** — half of all triage-level predictions across all classes are, on average, missed. It is the best baseline available, not a solution.
2. **It required the longest training time in this benchmark (11.2 seconds)**, though this is a one-off cost paid during model development, not during deployment, so its practical weight is low.
3. **It is a linear model**, and cannot capture interactions between features that a tree-based method might, in principle, exploit — though this benchmark found no evidence that the random forest actually exploited any such interaction to clinical benefit.

## Risks and Unknowns

- **We do not yet know whether the random forest's failure on ESI Level 1 is a fundamental data limitation (too few ESI 1 cases, 77 in the full dataset) or a fixable hyperparameter issue (e.g. class weighting, different tree depth).** This benchmark does not rule out the possibility that a properly tuned random forest could still outperform logistic regression on this metric.
- **Neither model is yet fit for clinical deployment.** A 0.400 recall on the most critical patient class means 6 in 10 ESI Level 1 patients would still be missed under the current logistic regression baseline. This memo recommends logistic regression as the *better of the two options benchmarked*, not as a deployment-ready system.

## Recommendation

Proceed to Phase 3 with **logistic regression**, not the random forest. Future development effort should focus on techniques that directly address class imbalance for the existing linear model — such as class weighting or a cost-sensitive decision threshold tuned specifically to raise ESI Level 1 recall — rather than pursuing additional model complexity that has not, in this benchmark, delivered any clinical benefit.
