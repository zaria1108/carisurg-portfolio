# Week 3 – Healthcare Workflows & Systems Thinking

## Objective
To map the current Emergency Department (ED) triage workflow, identify realistic points where an AI-assisted triage system could integrate, and refine the preliminary proposal with a systems-thinking lens grounded in clinical and operational constraints.

## Activities Completed
- Mapped the end-to-end ED triage workflow from patient arrival to disposition (Registration → Vitals Collection → Triage Nurse Assessment → Priority Assignment → Waiting Area Monitoring → Clinician Assessment → Disposition)
- Produced an initial workflow diagram and a refined version showing decision points, information flow, and handoffs
- Identified five AI plug-in points across the workflow, each scoped as decision *support* rather than decision replacement
- Defined three core workflow constraints that any AI intervention must respect, each paired with a design response and a measurable indicator
- Identified five clinical stakeholders and their primary concerns
- Expanded the literature review from seven to ten references, incorporating deployment- and constraint-focused studies
- Revised the preliminary proposal to add **Healthcare Workflow**, **AI Integration Points**, **Constraints**, and **Stakeholders** sections

## AI Integration Points
1. **Registration Support** – structures intake information into standard fields before assessment begins
2. **Observation Validation** – flags missing or unusual vital sign combinations before triage completion
3. **Triage Decision Support** – surfaces risk indicators alongside nurse assessment without replacing categorization
4. **Queue Monitoring** – identifies patients whose wait time and observations suggest reassessment
5. **Disposition Awareness** – surfaces relevant outcome indicators to support clinician decisions

## Workflow Constraints Identified

**Constraint 1: Sequential Information Capture Creates an Early Decision Blind Spot**
Prioritization may begin before full vitals and clinical context are available. The system must update recommendations dynamically and display confidence levels.

**Constraint 2: Multiple Handoffs Create Information Translation Risk**
Information gathered early may lose visibility later. The system must carry forward structured summaries instead of prompting repeated entry.

**Constraint 3: Queue Status Does Not Automatically Trigger Reassessment**
Patient condition can evolve while waiting. The system should generate reassessment prompts based on elapsed time and observations, without auto-reassigning urgency.

## Stakeholders
| Stakeholder | Top Concern |
|---|---|
| Triage Nurse | Maintaining assessment speed without duplicate documentation |
| Emergency Physician | Receiving reliable prioritization support |
| Patient | Fair and timely assessment |
| Hospital Administration | Improving patient flow without increasing workload |
| Clinical IT Team | Integration into existing infrastructure |

## Additional Literature Reviewed
8. Qualitative exploration of patient flow in a Caribbean emergency department (De Freitas et al., 2020)
9. Machine-learning-based electronic triage vs. Emergency Severity Index (Levin et al., 2018)
10. An overview of clinical decision support systems: benefits, risks, and strategies for success (Sutton et al., 2020)

## Deliverables
- [x] Workflow diagram with annotated AI plug-in points
- [x] Three candidate workflow constraints with design responses and measurements
- [x] Five stakeholders with top concerns identified
- [x] Literature review expanded (7 → 10 papers)
- [x] Refined preliminary proposal with systems-thinking section

## Reflection
This week shifted the project's focus from purely predictive performance to operational fit. Mapping the workflow revealed that information enters the ED process progressively rather than all at once, and that clinical decisions are often made on incomplete data. This reframed the proposed system's design priorities: dynamic updating, context preservation across handoffs, and reassessment prompts rather than automated reassignment. The exercise reinforced that a technically strong model still fails to deliver clinical value if it disregards documentation burden, clinician trust, and the realities of a busy triage station.
