# Delivery Plan & Risk Register

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-DELIVERY |
| Component name | Delivery Plan & Risk Register |
| Component type | Programme plan |
| Version | 1.0 |
| Status | Draft for review |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board; Engineering Director |
| Approvers | Engineering Director; Sponsor |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |

---

# 1. Purpose

The Phase Implementation Plan defined *what* to build and *in what order* but carried no timeline,
effort, staffing model, or risk register, so schedule feasibility could not be assessed. This plan
supplies indicative effort and staffing, makes the delivery risk explicit, and defines the
"thin governed thread" first increment that de-risks the foundation-first approach.

These figures are planning-grade order-of-magnitude estimates for a competent product engineering
organisation, not a commitment. They exist so the programme can be resourced and challenged. They
assume a green-field build, a modern cloud platform, and the reconciled specification set as scope.

# 2. Indicative effort and staffing

The scope is comparable to building an integrated ALM/governance platform (the combined surface of
an issue tracker, a requirements/V&V tool, a document-control system, a CI/CD provenance layer, a
release/CMDB system, and a security/GRC suite) on a custom governed-record substrate. That is a
multi-year programme.

| Phase block | Phases | Indicative team | Indicative duration |
|---|---|---|---|
| Foundation engineering | 0 setup | 1 platform squad (6–8) | 1–2 months |
| Substrate | 1–5 | 2 squads (12–16) | 7–11 months |
| Core operational modules | 6–8 | 2–3 squads (16–22) | 6–9 months |
| Delivery & assurance modules | 9–10 | 2 squads (12–16) | 5–8 months |
| Hardening & analytics | 11 | 1–2 squads (8–12) | 3–5 months |
| AI assistance | 12 | 1 squad + ML support (6–9) | 3–5 months |

Indicative total: roughly **24–40 months** of calendar time at a steady **18–28 engineers** plus
product, QA/test, design, security, and SRE roles, with phases overlapping where dependencies
allow. The single largest schedule risk sits in the substrate (Phases 3–4): immutable audit,
historical reconstruction, and graph-projection consistency are the hardest engineering in the
programme and everything else depends on them.

# 3. The foundation-first funding risk and how the thin thread addresses it

"No MVP / foundation-first" means Phases 0–5 deliver no end-user-facing module — the first
operational capability is Phase 6, potentially a year in. That is a defensible engineering posture
but a real funding and stakeholder-confidence risk, and it sits in tension with the agile
principle that every increment should extend an end-to-end capability.

The mitigation is the **thin governed thread**, scheduled at the end of Phase 2 / start of Phase 3,
before the full functional modules:

1. Pick one simple record type (a generic "controlled item").
2. Carry it end-to-end through the substrate as a single vertical slice: create → review → approve
   (`SPMS-WF-GOV`) → attach evidence (`SPMS-EVID-AUDIT`) → baseline (`SPMS-BASE-CCB`) → link
   (`SPMS-TRACE-GRAPH`) → emit events (`SPMS-INT-EVENT`) → audit and reconstruct historical state.
3. Expose it through a minimal UI and the public API.

This proves the substrate against real usage months earlier than Phase 6, gives stakeholders a
working, demonstrable governed-record loop to fund against, and surfaces integration problems in
the hardest components while they are still cheap to fix. It honours both planning documents: a
vertical slice that does not jump ahead of its substrate (see `SPMS-METHODOLOGY`).

# 4. Delivery risk register

| ID | Risk | Likelihood | Impact | Response |
|---|---|---|---|---|
| `RISK-001` | Substrate (audit/reconstruction/graph) underestimated; later modules blocked | High | High | Spike Phases 3–4 early; thin thread as proof; senior ownership; explicit performance gates per `SPMS-STD-SCALE` |
| `RISK-002` | Foundation-first delays user-visible value; sponsor confidence erodes | Medium | High | Thin governed thread; monthly demos of substrate capability; staged funding tied to phase exit criteria |
| `RISK-003` | Specifications re-diverge into parallel versions | Medium | High | Single register (`SPMS-INDEX`); linter in CI; domain model as sole source; controlled-change rule on shared docs |
| `RISK-004` | Graph projection vs relational store consistency defects | Medium | High | Reconciliation tooling (plan §18.4); projection-consistency tests; rebuild-and-compare in nightly pipeline |
| `RISK-005` | Scope creep across 19 components without prioritisation | High | Medium | "Required for minimal mode" flag per capability; Small-profile usable subset first; defer Should/Could |
| `RISK-006` | NFR targets unmet at Large profile | Medium | Medium | `SPMS-STD-SCALE` soak tests per release candidate; partitioning and worker scaling designed in, not retrofitted |
| `RISK-007` | AI assistance bypasses governance | Low | High | Human-in-the-loop enforced; AI writes proposals only; red-team tenant-leakage tests (`SPMS-AUTO-AI`) |
| `RISK-008` | Detail in superseded numbered specs lost during reconciliation | Medium | Medium | `DETAIL-HARVEST-BACKLOG`; superseded set retained read-only; harvest before each module's detailed design |
| `RISK-009` | Key-person dependency on substrate architects | Medium | Medium | Pair on substrate; ADRs; rotate review; document the hard parts first |
| `RISK-010` | Estimates treated as commitments | Medium | Medium | Re-estimate at each phase boundary from actuals; this plan is planning-grade only |

# 5. Recommended phasing adjustments

1. Insert the thin governed thread as an explicit milestone between Phases 2 and 3 (now reflected in
   the Phase Implementation Plan).
2. Keep a continuously usable Small-profile system from Phase 6 onward, even as later modules are
   built, rather than waiting for full programme completion.
3. Gate each phase exit on the per-phase exit criteria already in the plan plus a passing linter run
   and the relevant `SPMS-STD-SCALE` performance tests.
4. Re-baseline effort estimates at every phase boundary from measured velocity.
