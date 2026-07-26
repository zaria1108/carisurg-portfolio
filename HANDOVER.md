# Handover Document — CariSurg ED Triage Support Model
**Status: DRAFT OUTLINE — interim submission. Full prose to be completed for final submission.**

## 1. Project Summary
*(To write: one paragraph — what this model does, what dataset it's trained on, and what decision it supports at the point of ED triage. Draw from the Week 5 feasibility memo intro and Week 6 report intro.)*

## 2. Final Model Decision
- **Model:** Logistic Regression
- **One-sentence why:** *(To write — condense the Week 7 decision journal's reasoning into a single sentence, e.g. "Chosen because it was the only model benchmarked with non-zero recall on the most critical patient class, while also being the fastest and most explainable option.")*
- Full reasoning: `docs/decisions/2026-week-7-model-choice.md`

## 3. How to Run
```bash
python scripts/train.py --config config.yaml
```
*(To expand: prerequisites — Python version, `pip install -r requirements.txt`, where to place the raw data file, expected runtime.)*

## 4. Where the Data Lives
*(To write: data source, governance/de-identification status, who owns access, and where `raw_path` in config.yaml should point on Mercer's systems.)*

## 5. Known Limitations
- *(To write — likely candidates drawn from Weeks 5-7: modest ESI-1 recall (~0.33–0.40, still misses roughly 6 in 10 critical patients), single-snapshot data (not a time-series, can't fully validate "earlier deterioration detection"), representativeness of a US academic-hospital sample for a Caribbean ED.)*
- *(To write)*
- *(To write)*

---
**Next steps before final submission:** complete all `(To write)` sections above in full prose; this outline exists to confirm the structure is right before investing in the writing.
