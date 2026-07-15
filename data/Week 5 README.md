# Week 5 – Clinical Data Literacy & Feasibility Assessment

## Objective
To assess whether the Yale EMMLC triage extract is a feasible foundation for the proposed AI-assisted ED triage system, by developing clinical literacy in the dataset's structure and producing an honest, evidence-based feasibility memo for the ED Board.

## Activities Completed
- Loaded and profiled the Yale EMMLC triage extract (55,121 de-identified adult ED encounters, 225 features)
- Named the three feature families — identifiers & outcomes, arrival vitals, and ~200 chief-complaint flags — and documented the clinical meaning of each
- Read the triage vitals against normal adult ranges and identified the Fahrenheit unit trap in `triage_vital_temp`
- Grouped the 200 sparse chief-complaint flags into ~12 clinical body systems and ranked complaint prevalence
- Confirmed `esi` (Triage_Level) as the model target and explained the five ESI levels
- Identified `disposition` and `previousdispo` as leakage columns, excluded from any triage-time model input
- Produced six exploratory visualisations: missingness, ESI class balance & age, race/ethnicity demographics, top chief complaints, vitals-by-ESI boxplots, and a vitals/ESI correlation heatmap
- Added a seventh equity plot (ESI distribution within race category) to directly test the project's bias-monitoring commitment
- Ran a formal outlier audit (statistical IQR outliers vs. clinically impossible values) across all seven vitals — confirmed zero impossible readings
- Wrote and committed a three-page feasibility memo with verdict, dataset summary, top concerns, reasons to proceed, caveats, and a preliminary ten-feature shortlist

## Feasibility Verdict
**Proceed to a baseline triage model, with caveats.** The dataset provides a real, complete triage label (`esi`, 0% missing), complete and physiologically plausible vitals, and a documented, reproducible analysis pipeline — sufficient grounds to move to modelling in Week 6.

## Top Three Concerns

| Concern | Detail |
|---|---|
| Outcome leakage | `disposition` and `previousdispo` are known only after triage; excluded from all model inputs |
| Demographic imbalance & potential bias | ESI distribution is not uniform across race categories; smallest subgroups (e.g. n=20) are too small for reliable conclusions |
| Representativeness for a Caribbean ED | Single US academic-hospital sample; case-mix, demographics, and access patterns may not transfer to Mercer General |

## Additional Data-Quality Findings
- Missingness: 0% across all 225 columns (both structured fields and chief-complaint flags)
- Outliers: zero clinically impossible vital-sign values across all seven vitals; statistical outliers present but represent real extreme presentations, not data errors
- 86.9% of patients present with only a single chief complaint, keeping the feature space tractable for an explainable model

## Deliverables
- [x] EDA notebook (`notebooks/Week5_Tutorial1_Clinical_Data_Literacy.ipynb`)
- [x] Missingness heatmap and table (`docs/01_missingness.png`)
- [x] Six core EDA visualisations + equity plot (`docs/`)
- [x] Outlier audit (statistical vs. clinically impossible, per vital)
- [x] Three-page feasibility memo (`docs/Feasibility_Memo.docx`)
- [x] Preliminary ten-feature shortlist, ranked by correlation with `esi`

## Reflection
This week reframed the project around a single question: before building anything, do we actually understand what each column means? The most valuable finding wasn't a statistic — it was the discipline of naming what the data *can't* tell us as clearly as what it can. The equity plot was the clearest example: rather than treating a clean-looking demographic breakdown as reassuring, breaking it down by ESI level surfaced a pattern that needs monitoring, not celebrating. The Fahrenheit trap and the single-snapshot-not-timeseries caveat were smaller but equally important reminders that literacy has to come before modelling — a model trained on a misunderstood column is not safer for being accurate.
