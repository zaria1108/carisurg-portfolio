# Week 4 – Ethics, Safety & Risk Awareness in Healthcare Technology

## Objective
To identify and document the safety, ethical, operational, and equity risks associated with deploying the proposed AI-assisted ED triage system, and to develop a defensible personal stance on AI augmentation versus replacement in clinical work.

## Activities Completed
- Built a risk register of five named risks spanning AI-technical, operational, ethical, and equity categories, each with likelihood, impact, mitigation, and a measurable signal of success
- Wrote a risk memo detailing the top three priority risks in plain language
- Researched and documented a real-world AI-harm case study (Epic Sepsis Prediction Model) with a root-cause analysis
- Expanded the literature review from ten to fifteen papers, with new emphasis on explainability, transparency, and ethics in clinical AI decision support
- Added a **Risk Analysis** section to the preliminary proposal, incorporating the risk register and memo

## Risk Register

| Risk Name | Category | Likelihood | Impact | Mitigation | Signal of Success |
|---|---|---|---|---|---|
| Recommendation Instability from Progressive Data Entry | AI-Technical | High | High | Delay final recommendations until minimum observations are available; continuously update outputs | Reduction in recommendation changes after complete triage |
| Context Loss Across Workflow Handoffs | Operational | High | High | Preserve structured summaries across registration, triage, and clinician review | Reduction in repeated information collection |
| Alert Fatigue During Queue Monitoring | Operational | Medium | High | Restrict alerts to escalation thresholds; suppress repetitive notifications | Sustained clinician response to reassessment alerts |
| Automation Bias During Triage Support | Ethical | Medium | High | Require clinician confirmation; display supporting factors for recommendations | Low override acceptance without independent review |
| Unequal Performance Across Hospital Sites | Equity | Medium | High | Validate models separately across hospitals before rollout | Comparable performance across deployment sites |

## Risk Memo – Top Three Priority Risks

**1. Recommendation Instability from Progressive Data Entry**
Information in the ED workflow becomes available progressively rather than all at once. Generating recommendations too early can cause outputs to shift substantially once further observations arrive, undermining clinician trust.
*Mitigation:* require minimum observation thresholds before generating recommendations and refresh outputs dynamically.

**2. Context Loss Across Workflow Handoffs**
Patient information moves across administrative staff, triage nurses, and clinicians. Details captured early may lose visibility later, risking incomplete recommendations.
*Mitigation:* carry structured summaries forward instead of requiring repeated data collection.

**3. Automation Bias During Triage Support**
Under operational pressure, clinicians may over-rely on AI recommendations, especially if outputs appear precise or lack uncertainty indicators.
*Mitigation:* display confidence information, preserve clinician authority, and require confirmation before recommendations are accepted.

## Documented AI-Harm Case Study: Epic Sepsis Prediction Model

**What happened:** A machine-learning sepsis prediction system deployed across hospitals identified substantially fewer at-risk cases than expected and delivered limited practical benefit in real-world use.

**Root cause:** Performance diverged from retrospective testing due to differences between training conditions and real deployment conditions, delayed data availability, and incorrect assumptions about how clinicians would act on alerts.

**What failed:**
- Performance did not generalize as expected
- Operational assumptions were not validated pre-deployment
- Post-deployment monitoring was insufficient

**What would have reduced harm:** prospective validation, site-level evaluation, continuous post-rollout monitoring, and human review before escalation.

**Relevance to this project:** Reinforces that predictive performance alone is not sufficient — workflow fit, data readiness, monitoring, and clinician oversight are equally critical to safe deployment.

## Additional Literature Reviewed
11. The ethical requirement of explainability for AI-DSS in healthcare: a systematic review of reasons (Freyer et al., 2024)
12. The role of explainability in AI-supported medical decision-making (Gerdes, 2024)
13. Should AI models be explainable to clinicians? (Abgrall et al., 2024)
14. A survey of explainable artificial intelligence in healthcare: concepts, applications, and challenges (Mienye et al., 2024)
15. Trusting AI made decisions in healthcare by making them explainable (Žlahtič et al., 2024)

## Deliverables
- [x] Risk register (5 risks, `docs/risk-register.md`)
- [x] Risk memo covering top 3 priority risks
- [x] Documented AI-harm case study with root-cause analysis
- [x] Literature review expanded (10 → 15 papers)
- [x] Refined preliminary proposal with Risk Analysis section
- [ ] LinkedIn post on AI augmentation vs. replacement in clinical work

## Reflection
This week required confronting the uncomfortable side of the project: where the proposed system could fail, and who would bear the cost of that failure. Building the risk register made clear that the most dangerous risks are not always the most technical ones — automation bias and context loss are as much about human behavior under pressure as they are about model performance. The Epic Sepsis Model case study was a sobering reminder that strong retrospective results do not guarantee real-world benefit, and that monitoring and validation after deployment matter as much as design before it. This has sharpened the proposal's emphasis on dynamic confidence reporting, mandatory clinician confirmation, and site-level validation rather than a single national rollout assumption.
