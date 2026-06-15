# Scope & Prioritisation Register

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-SCOPE |
| Component name | Scope & Prioritisation Register |
| Component type | Programme register (controlling document) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

This register is the single authoritative rollup of capability priorities across all 19 SPMS
components. It implements the named mitigation for `RISK-005` in `SPMS-DELIVERY` (scope creep
across 19 components without prioritisation) by making the following structural:

- A central rollup table (§2) aggregates the `Priority` and `Required for minimal mode?` values
  declared per-capability in each component specification. The component specifications remain
  the authoritative source; this register is the rollup. If a discrepancy exists, the component
  specification governs and this register must be updated.
- A governance-profile × capability-inclusion matrix (§3) defines which priority tiers are in
  scope for each governance profile, replacing per-project ad hoc decisions with a cross-tenant
  policy.
- The minimal-mode capability set (§4) lists every `Required for minimal mode? = Yes` capability
  explicitly and is required to agree with `SPMS-STD-SCALE §5`. Any disagreement is a
  conformance defect in this register.
- Per-phase scope locks (§5) prevent new capabilities from being injected mid-phase.
- A deferral register (§6) records every explicitly deferred Should/Could capability as a
  managed decision.

**Note on rollup generation.** The §2 table is generated from the component specifications by
the extraction script at `tools/gen_scope_rollup.py` (or equivalent). The linter
(`tools/spec_lint.py`) may be extended to check rollup↔spec consistency automatically. A
human reviewer must confirm the rollup at each phase boundary.

# 2. Capability Rollup Table

This table aggregates the `Capability ID`, `Priority`, and `Required for minimal mode?` columns
from the §4.1 Capability Summary table of each component specification. The `Phase` column
matches the component's implementation phase in `SPMS-INDEX §3`.

**Total capabilities: 158** across 19 components.

| Capability ID | Component | Priority | Required for minimal mode? | Phase |
|---|---|---|---|---|
| `SPMS-PLAT-CORE-CAP-001` | `SPMS-PLAT-CORE` | Must | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-002` | `SPMS-PLAT-CORE` | Must | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-003` | `SPMS-PLAT-CORE` | Must | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-004` | `SPMS-PLAT-CORE` | Must | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-005` | `SPMS-PLAT-CORE` | Should | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-006` | `SPMS-PLAT-CORE` | Should | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-007` | `SPMS-PLAT-CORE` | Should | Yes | 1 |
| `SPMS-PLAT-CORE-CAP-008` | `SPMS-PLAT-CORE` | Should | Yes | 1 |
| `SPMS-WF-GOV-CAP-001` | `SPMS-WF-GOV` | Must | Yes | 2 |
| `SPMS-WF-GOV-CAP-002` | `SPMS-WF-GOV` | Must | Yes | 2 |
| `SPMS-WF-GOV-CAP-003` | `SPMS-WF-GOV` | Must | Yes | 2 |
| `SPMS-WF-GOV-CAP-004` | `SPMS-WF-GOV` | Must | Yes | 2 |
| `SPMS-WF-GOV-CAP-005` | `SPMS-WF-GOV` | Should | Yes | 2 |
| `SPMS-WF-GOV-CAP-006` | `SPMS-WF-GOV` | Should | Yes | 2 |
| `SPMS-WF-GOV-CAP-007` | `SPMS-WF-GOV` | Should | Yes | 2 |
| `SPMS-WF-GOV-CAP-008` | `SPMS-WF-GOV` | Should | Yes | 2 |
| `SPMS-BASE-CCB-CAP-001` | `SPMS-BASE-CCB` | Must | Yes | 3 |
| `SPMS-BASE-CCB-CAP-002` | `SPMS-BASE-CCB` | Must | Yes | 3 |
| `SPMS-BASE-CCB-CAP-003` | `SPMS-BASE-CCB` | Must | Yes | 3 |
| `SPMS-BASE-CCB-CAP-004` | `SPMS-BASE-CCB` | Must | Yes | 3 |
| `SPMS-BASE-CCB-CAP-005` | `SPMS-BASE-CCB` | Must | Yes | 3 |
| `SPMS-BASE-CCB-CAP-006` | `SPMS-BASE-CCB` | Must | No | 3 |
| `SPMS-BASE-CCB-CAP-007` | `SPMS-BASE-CCB` | Must | No | 3 |
| `SPMS-BASE-CCB-CAP-008` | `SPMS-BASE-CCB` | Must | No | 3 |
| `SPMS-BASE-CCB-CAP-009` | `SPMS-BASE-CCB` | Must | No | 3 |
| `SPMS-BASE-CCB-CAP-010` | `SPMS-BASE-CCB` | Must | No | 3 |
| `SPMS-DATA-STORE-CAP-001` | `SPMS-DATA-STORE` | Must | Yes | 3 |
| `SPMS-DATA-STORE-CAP-002` | `SPMS-DATA-STORE` | Must | Yes | 3 |
| `SPMS-DATA-STORE-CAP-003` | `SPMS-DATA-STORE` | Must | Yes | 3 |
| `SPMS-DATA-STORE-CAP-004` | `SPMS-DATA-STORE` | Must | Yes | 3 |
| `SPMS-DATA-STORE-CAP-005` | `SPMS-DATA-STORE` | Must | Yes | 3 |
| `SPMS-DATA-STORE-CAP-006` | `SPMS-DATA-STORE` | Must | No | 3 |
| `SPMS-DATA-STORE-CAP-007` | `SPMS-DATA-STORE` | Must | No | 3 |
| `SPMS-DATA-STORE-CAP-008` | `SPMS-DATA-STORE` | Must | No | 3 |
| `SPMS-DATA-STORE-CAP-009` | `SPMS-DATA-STORE` | Must | No | 3 |
| `SPMS-DATA-STORE-CAP-010` | `SPMS-DATA-STORE` | Must | No | 3 |
| `SPMS-EVID-AUDIT-CAP-001` | `SPMS-EVID-AUDIT` | Must | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-002` | `SPMS-EVID-AUDIT` | Must | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-003` | `SPMS-EVID-AUDIT` | Must | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-004` | `SPMS-EVID-AUDIT` | Must | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-005` | `SPMS-EVID-AUDIT` | Should | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-006` | `SPMS-EVID-AUDIT` | Should | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-007` | `SPMS-EVID-AUDIT` | Should | Yes | 3 |
| `SPMS-EVID-AUDIT-CAP-008` | `SPMS-EVID-AUDIT` | Should | Yes | 3 |
| `SPMS-TRACE-GRAPH-CAP-001` | `SPMS-TRACE-GRAPH` | Must | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-002` | `SPMS-TRACE-GRAPH` | Must | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-003` | `SPMS-TRACE-GRAPH` | Must | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-004` | `SPMS-TRACE-GRAPH` | Must | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-005` | `SPMS-TRACE-GRAPH` | Should | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-006` | `SPMS-TRACE-GRAPH` | Should | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-007` | `SPMS-TRACE-GRAPH` | Should | Yes | 4 |
| `SPMS-TRACE-GRAPH-CAP-008` | `SPMS-TRACE-GRAPH` | Should | Yes | 4 |
| `SPMS-INT-EVENT-CAP-001` | `SPMS-INT-EVENT` | Must | Yes | 5 |
| `SPMS-INT-EVENT-CAP-002` | `SPMS-INT-EVENT` | Must | Yes | 5 |
| `SPMS-INT-EVENT-CAP-003` | `SPMS-INT-EVENT` | Must | Yes | 5 |
| `SPMS-INT-EVENT-CAP-004` | `SPMS-INT-EVENT` | Must | Yes | 5 |
| `SPMS-INT-EVENT-CAP-005` | `SPMS-INT-EVENT` | Must | Yes | 5 |
| `SPMS-INT-EVENT-CAP-006` | `SPMS-INT-EVENT` | Must | No | 5 |
| `SPMS-INT-EVENT-CAP-007` | `SPMS-INT-EVENT` | Must | No | 5 |
| `SPMS-INT-EVENT-CAP-008` | `SPMS-INT-EVENT` | Must | No | 5 |
| `SPMS-INT-EVENT-CAP-009` | `SPMS-INT-EVENT` | Must | No | 5 |
| `SPMS-INT-EVENT-CAP-010` | `SPMS-INT-EVENT` | Must | No | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-001` | `SPMS-REPORT-ANALYTICS` | Must | Yes | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-002` | `SPMS-REPORT-ANALYTICS` | Must | Yes | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-003` | `SPMS-REPORT-ANALYTICS` | Must | Yes | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-004` | `SPMS-REPORT-ANALYTICS` | Must | Yes | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-005` | `SPMS-REPORT-ANALYTICS` | Should | No | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-006` | `SPMS-REPORT-ANALYTICS` | Should | No | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-007` | `SPMS-REPORT-ANALYTICS` | Should | No | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-008` | `SPMS-REPORT-ANALYTICS` | Should | No | 5 |
| `SPMS-DOC-KM-CAP-001` | `SPMS-DOC-KM` | Must | Yes | 6 |
| `SPMS-DOC-KM-CAP-002` | `SPMS-DOC-KM` | Must | Yes | 6 |
| `SPMS-DOC-KM-CAP-003` | `SPMS-DOC-KM` | Must | Yes | 6 |
| `SPMS-DOC-KM-CAP-004` | `SPMS-DOC-KM` | Must | Yes | 6 |
| `SPMS-DOC-KM-CAP-005` | `SPMS-DOC-KM` | Should | No | 6 |
| `SPMS-DOC-KM-CAP-006` | `SPMS-DOC-KM` | Should | No | 6 |
| `SPMS-DOC-KM-CAP-007` | `SPMS-DOC-KM` | Should | No | 6 |
| `SPMS-DOC-KM-CAP-008` | `SPMS-DOC-KM` | Should | No | 6 |
| `SPMS-ISS-CHG-CAP-001` | `SPMS-ISS-CHG` | Must | Yes | 6 |
| `SPMS-ISS-CHG-CAP-002` | `SPMS-ISS-CHG` | Must | Yes | 6 |
| `SPMS-ISS-CHG-CAP-003` | `SPMS-ISS-CHG` | Must | Yes | 6 |
| `SPMS-ISS-CHG-CAP-004` | `SPMS-ISS-CHG` | Must | Yes | 6 |
| `SPMS-ISS-CHG-CAP-005` | `SPMS-ISS-CHG` | Should | No | 6 |
| `SPMS-ISS-CHG-CAP-006` | `SPMS-ISS-CHG` | Should | No | 6 |
| `SPMS-ISS-CHG-CAP-007` | `SPMS-ISS-CHG` | Should | No | 6 |
| `SPMS-ISS-CHG-CAP-008` | `SPMS-ISS-CHG` | Should | No | 6 |
| `SPMS-WP-PLAN-CAP-001` | `SPMS-WP-PLAN` | Must | Yes | 6 |
| `SPMS-WP-PLAN-CAP-002` | `SPMS-WP-PLAN` | Must | Yes | 6 |
| `SPMS-WP-PLAN-CAP-003` | `SPMS-WP-PLAN` | Must | Yes | 6 |
| `SPMS-WP-PLAN-CAP-004` | `SPMS-WP-PLAN` | Must | Yes | 6 |
| `SPMS-WP-PLAN-CAP-005` | `SPMS-WP-PLAN` | Should | No | 6 |
| `SPMS-WP-PLAN-CAP-006` | `SPMS-WP-PLAN` | Should | No | 6 |
| `SPMS-WP-PLAN-CAP-007` | `SPMS-WP-PLAN` | Should | No | 6 |
| `SPMS-WP-PLAN-CAP-008` | `SPMS-WP-PLAN` | Should | No | 6 |
| `SPMS-REQ-MGMT-CAP-001` | `SPMS-REQ-MGMT` | Must | Yes | 7 |
| `SPMS-REQ-MGMT-CAP-002` | `SPMS-REQ-MGMT` | Must | Yes | 7 |
| `SPMS-REQ-MGMT-CAP-003` | `SPMS-REQ-MGMT` | Must | Yes | 7 |
| `SPMS-REQ-MGMT-CAP-004` | `SPMS-REQ-MGMT` | Must | Yes | 7 |
| `SPMS-REQ-MGMT-CAP-005` | `SPMS-REQ-MGMT` | Should | No | 7 |
| `SPMS-REQ-MGMT-CAP-006` | `SPMS-REQ-MGMT` | Should | No | 7 |
| `SPMS-REQ-MGMT-CAP-007` | `SPMS-REQ-MGMT` | Should | No | 7 |
| `SPMS-REQ-MGMT-CAP-008` | `SPMS-REQ-MGMT` | Should | No | 7 |
| `SPMS-TEST-VV-CAP-001` | `SPMS-TEST-VV` | Must | Yes | 7 |
| `SPMS-TEST-VV-CAP-002` | `SPMS-TEST-VV` | Must | Yes | 7 |
| `SPMS-TEST-VV-CAP-003` | `SPMS-TEST-VV` | Must | Yes | 7 |
| `SPMS-TEST-VV-CAP-004` | `SPMS-TEST-VV` | Must | Yes | 7 |
| `SPMS-TEST-VV-CAP-005` | `SPMS-TEST-VV` | Should | No | 7 |
| `SPMS-TEST-VV-CAP-006` | `SPMS-TEST-VV` | Should | No | 7 |
| `SPMS-TEST-VV-CAP-007` | `SPMS-TEST-VV` | Should | No | 7 |
| `SPMS-TEST-VV-CAP-008` | `SPMS-TEST-VV` | Should | No | 7 |
| `SPMS-CICD-CAP-001` | `SPMS-CICD` | Must | Yes | 8 |
| `SPMS-CICD-CAP-002` | `SPMS-CICD` | Must | Yes | 8 |
| `SPMS-CICD-CAP-003` | `SPMS-CICD` | Must | Yes | 8 |
| `SPMS-CICD-CAP-004` | `SPMS-CICD` | Must | Yes | 8 |
| `SPMS-CICD-CAP-005` | `SPMS-CICD` | Should | No | 8 |
| `SPMS-CICD-CAP-006` | `SPMS-CICD` | Should | No | 8 |
| `SPMS-CICD-CAP-007` | `SPMS-CICD` | Should | No | 8 |
| `SPMS-CICD-CAP-008` | `SPMS-CICD` | Should | No | 8 |
| `SPMS-CFG-ASSET-CAP-001` | `SPMS-CFG-ASSET` | Must | Yes | 9 |
| `SPMS-CFG-ASSET-CAP-002` | `SPMS-CFG-ASSET` | Must | Yes | 9 |
| `SPMS-CFG-ASSET-CAP-003` | `SPMS-CFG-ASSET` | Must | Yes | 9 |
| `SPMS-CFG-ASSET-CAP-004` | `SPMS-CFG-ASSET` | Must | Yes | 9 |
| `SPMS-CFG-ASSET-CAP-005` | `SPMS-CFG-ASSET` | Should | No | 9 |
| `SPMS-CFG-ASSET-CAP-006` | `SPMS-CFG-ASSET` | Should | No | 9 |
| `SPMS-CFG-ASSET-CAP-007` | `SPMS-CFG-ASSET` | Should | No | 9 |
| `SPMS-CFG-ASSET-CAP-008` | `SPMS-CFG-ASSET` | Should | No | 9 |
| `SPMS-REL-DEP-CAP-001` | `SPMS-REL-DEP` | Must | Yes | 9 |
| `SPMS-REL-DEP-CAP-002` | `SPMS-REL-DEP` | Must | Yes | 9 |
| `SPMS-REL-DEP-CAP-003` | `SPMS-REL-DEP` | Must | Yes | 9 |
| `SPMS-REL-DEP-CAP-004` | `SPMS-REL-DEP` | Must | Yes | 9 |
| `SPMS-REL-DEP-CAP-005` | `SPMS-REL-DEP` | Should | No | 9 |
| `SPMS-REL-DEP-CAP-006` | `SPMS-REL-DEP` | Should | No | 9 |
| `SPMS-REL-DEP-CAP-007` | `SPMS-REL-DEP` | Should | No | 9 |
| `SPMS-REL-DEP-CAP-008` | `SPMS-REL-DEP` | Should | No | 9 |
| `SPMS-PROD-ASSUR-CAP-001` | `SPMS-PROD-ASSUR` | Must | Yes | 10 |
| `SPMS-PROD-ASSUR-CAP-002` | `SPMS-PROD-ASSUR` | Must | Yes | 10 |
| `SPMS-PROD-ASSUR-CAP-003` | `SPMS-PROD-ASSUR` | Must | Yes | 10 |
| `SPMS-PROD-ASSUR-CAP-004` | `SPMS-PROD-ASSUR` | Must | Yes | 10 |
| `SPMS-PROD-ASSUR-CAP-005` | `SPMS-PROD-ASSUR` | Should | No | 10 |
| `SPMS-PROD-ASSUR-CAP-006` | `SPMS-PROD-ASSUR` | Should | No | 10 |
| `SPMS-PROD-ASSUR-CAP-007` | `SPMS-PROD-ASSUR` | Should | No | 10 |
| `SPMS-PROD-ASSUR-CAP-008` | `SPMS-PROD-ASSUR` | Should | No | 10 |
| `SPMS-SEC-COMP-CAP-001` | `SPMS-SEC-COMP` | Must | Yes | 10 |
| `SPMS-SEC-COMP-CAP-002` | `SPMS-SEC-COMP` | Must | Yes | 10 |
| `SPMS-SEC-COMP-CAP-003` | `SPMS-SEC-COMP` | Must | Yes | 10 |
| `SPMS-SEC-COMP-CAP-004` | `SPMS-SEC-COMP` | Must | Yes | 10 |
| `SPMS-SEC-COMP-CAP-005` | `SPMS-SEC-COMP` | Should | No | 10 |
| `SPMS-SEC-COMP-CAP-006` | `SPMS-SEC-COMP` | Should | No | 10 |
| `SPMS-SEC-COMP-CAP-007` | `SPMS-SEC-COMP` | Should | No | 10 |
| `SPMS-SEC-COMP-CAP-008` | `SPMS-SEC-COMP` | Should | No | 10 |
| `SPMS-AUTO-AI-CAP-001` | `SPMS-AUTO-AI` | Must | Yes | 12 |
| `SPMS-AUTO-AI-CAP-002` | `SPMS-AUTO-AI` | Must | Yes | 12 |
| `SPMS-AUTO-AI-CAP-003` | `SPMS-AUTO-AI` | Must | Yes | 12 |
| `SPMS-AUTO-AI-CAP-004` | `SPMS-AUTO-AI` | Must | Yes | 12 |
| `SPMS-AUTO-AI-CAP-005` | `SPMS-AUTO-AI` | Should | No | 12 |
| `SPMS-AUTO-AI-CAP-006` | `SPMS-AUTO-AI` | Should | No | 12 |
| `SPMS-AUTO-AI-CAP-007` | `SPMS-AUTO-AI` | Should | No | 12 |
| `SPMS-AUTO-AI-CAP-008` | `SPMS-AUTO-AI` | Should | No | 12 |

# 3. Governance-Profile × Capability Inclusion Matrix

This matrix defines which capability priority tiers are in scope for each governance profile.
Profiles are defined in `SPMS-WF-GOV §8.1`. The minimal deployment profile is defined in
`SPMS-STD-SCALE §5`.

| Governance Profile | Must | Should | Could | Notes |
|---|---|---|---|---|
| Lightweight | In scope | Out of scope | Out of scope | Minimal admin overhead; no automated or batch approvals |
| Low-risk bulk | In scope | Out of scope | Out of scope | Must-tier capabilities plus automated rule-based approval for whitelisted bulk operations |
| Standard | In scope | In scope | Out of scope | Full human review for all controlled changes |
| Controlled | In scope | In scope | Selected only | Could-tier capabilities require explicit project-level opt-in and waiver |
| Critical | In scope | In scope | In scope | All capabilities active; strictest gate set; full audit trail mandatory |

**Conformance rule.** A deployment operating at a given governance profile must have implemented
(or deferred with a managed decision per §6) every capability within the in-scope tiers for that
profile before being used for controlled governance activities. Deferred capabilities in an
in-scope tier must be tracked in the deferral register (§6).

# 4. Minimal-Mode Capability Set

The 95 capabilities listed below carry `Required for minimal mode? = Yes` in their source
specifications. This set defines the functional scope of a minimal SPMS deployment and must
agree with `SPMS-STD-SCALE §5`. Any capability present in `SPMS-STD-SCALE §5` but absent here,
or vice versa, is a conformance defect that must be resolved before Phase 6 exit.

**Note on Should-priority minimal capabilities.** Several capabilities are `Priority = Should`
but `Required for minimal mode? = Yes`. This reflects deliberate decisions in the source
specifications that certain Should-tier capabilities are foundational to correct operation of
the minimal substrate (e.g. notification substrate in `SPMS-PLAT-CORE`, evidence freshness in
`SPMS-EVID-AUDIT`, and graph snapshot support in `SPMS-TRACE-GRAPH`). These capabilities are
required in a minimal deployment despite their Should priority.

| Capability ID | Component | Priority | Phase |
|---|---|---|---|
| `SPMS-PLAT-CORE-CAP-001` | `SPMS-PLAT-CORE` | Must | 1 |
| `SPMS-PLAT-CORE-CAP-002` | `SPMS-PLAT-CORE` | Must | 1 |
| `SPMS-PLAT-CORE-CAP-003` | `SPMS-PLAT-CORE` | Must | 1 |
| `SPMS-PLAT-CORE-CAP-004` | `SPMS-PLAT-CORE` | Must | 1 |
| `SPMS-PLAT-CORE-CAP-005` | `SPMS-PLAT-CORE` | Should | 1 |
| `SPMS-PLAT-CORE-CAP-006` | `SPMS-PLAT-CORE` | Should | 1 |
| `SPMS-PLAT-CORE-CAP-007` | `SPMS-PLAT-CORE` | Should | 1 |
| `SPMS-PLAT-CORE-CAP-008` | `SPMS-PLAT-CORE` | Should | 1 |
| `SPMS-WF-GOV-CAP-001` | `SPMS-WF-GOV` | Must | 2 |
| `SPMS-WF-GOV-CAP-002` | `SPMS-WF-GOV` | Must | 2 |
| `SPMS-WF-GOV-CAP-003` | `SPMS-WF-GOV` | Must | 2 |
| `SPMS-WF-GOV-CAP-004` | `SPMS-WF-GOV` | Must | 2 |
| `SPMS-WF-GOV-CAP-005` | `SPMS-WF-GOV` | Should | 2 |
| `SPMS-WF-GOV-CAP-006` | `SPMS-WF-GOV` | Should | 2 |
| `SPMS-WF-GOV-CAP-007` | `SPMS-WF-GOV` | Should | 2 |
| `SPMS-WF-GOV-CAP-008` | `SPMS-WF-GOV` | Should | 2 |
| `SPMS-BASE-CCB-CAP-001` | `SPMS-BASE-CCB` | Must | 3 |
| `SPMS-BASE-CCB-CAP-002` | `SPMS-BASE-CCB` | Must | 3 |
| `SPMS-BASE-CCB-CAP-003` | `SPMS-BASE-CCB` | Must | 3 |
| `SPMS-BASE-CCB-CAP-004` | `SPMS-BASE-CCB` | Must | 3 |
| `SPMS-BASE-CCB-CAP-005` | `SPMS-BASE-CCB` | Must | 3 |
| `SPMS-DATA-STORE-CAP-001` | `SPMS-DATA-STORE` | Must | 3 |
| `SPMS-DATA-STORE-CAP-002` | `SPMS-DATA-STORE` | Must | 3 |
| `SPMS-DATA-STORE-CAP-003` | `SPMS-DATA-STORE` | Must | 3 |
| `SPMS-DATA-STORE-CAP-004` | `SPMS-DATA-STORE` | Must | 3 |
| `SPMS-DATA-STORE-CAP-005` | `SPMS-DATA-STORE` | Must | 3 |
| `SPMS-EVID-AUDIT-CAP-001` | `SPMS-EVID-AUDIT` | Must | 3 |
| `SPMS-EVID-AUDIT-CAP-002` | `SPMS-EVID-AUDIT` | Must | 3 |
| `SPMS-EVID-AUDIT-CAP-003` | `SPMS-EVID-AUDIT` | Must | 3 |
| `SPMS-EVID-AUDIT-CAP-004` | `SPMS-EVID-AUDIT` | Must | 3 |
| `SPMS-EVID-AUDIT-CAP-005` | `SPMS-EVID-AUDIT` | Should | 3 |
| `SPMS-EVID-AUDIT-CAP-006` | `SPMS-EVID-AUDIT` | Should | 3 |
| `SPMS-EVID-AUDIT-CAP-007` | `SPMS-EVID-AUDIT` | Should | 3 |
| `SPMS-EVID-AUDIT-CAP-008` | `SPMS-EVID-AUDIT` | Should | 3 |
| `SPMS-TRACE-GRAPH-CAP-001` | `SPMS-TRACE-GRAPH` | Must | 4 |
| `SPMS-TRACE-GRAPH-CAP-002` | `SPMS-TRACE-GRAPH` | Must | 4 |
| `SPMS-TRACE-GRAPH-CAP-003` | `SPMS-TRACE-GRAPH` | Must | 4 |
| `SPMS-TRACE-GRAPH-CAP-004` | `SPMS-TRACE-GRAPH` | Must | 4 |
| `SPMS-TRACE-GRAPH-CAP-005` | `SPMS-TRACE-GRAPH` | Should | 4 |
| `SPMS-TRACE-GRAPH-CAP-006` | `SPMS-TRACE-GRAPH` | Should | 4 |
| `SPMS-TRACE-GRAPH-CAP-007` | `SPMS-TRACE-GRAPH` | Should | 4 |
| `SPMS-TRACE-GRAPH-CAP-008` | `SPMS-TRACE-GRAPH` | Should | 4 |
| `SPMS-INT-EVENT-CAP-001` | `SPMS-INT-EVENT` | Must | 5 |
| `SPMS-INT-EVENT-CAP-002` | `SPMS-INT-EVENT` | Must | 5 |
| `SPMS-INT-EVENT-CAP-003` | `SPMS-INT-EVENT` | Must | 5 |
| `SPMS-INT-EVENT-CAP-004` | `SPMS-INT-EVENT` | Must | 5 |
| `SPMS-INT-EVENT-CAP-005` | `SPMS-INT-EVENT` | Must | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-001` | `SPMS-REPORT-ANALYTICS` | Must | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-002` | `SPMS-REPORT-ANALYTICS` | Must | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-003` | `SPMS-REPORT-ANALYTICS` | Must | 5 |
| `SPMS-REPORT-ANALYTICS-CAP-004` | `SPMS-REPORT-ANALYTICS` | Must | 5 |
| `SPMS-DOC-KM-CAP-001` | `SPMS-DOC-KM` | Must | 6 |
| `SPMS-DOC-KM-CAP-002` | `SPMS-DOC-KM` | Must | 6 |
| `SPMS-DOC-KM-CAP-003` | `SPMS-DOC-KM` | Must | 6 |
| `SPMS-DOC-KM-CAP-004` | `SPMS-DOC-KM` | Must | 6 |
| `SPMS-ISS-CHG-CAP-001` | `SPMS-ISS-CHG` | Must | 6 |
| `SPMS-ISS-CHG-CAP-002` | `SPMS-ISS-CHG` | Must | 6 |
| `SPMS-ISS-CHG-CAP-003` | `SPMS-ISS-CHG` | Must | 6 |
| `SPMS-ISS-CHG-CAP-004` | `SPMS-ISS-CHG` | Must | 6 |
| `SPMS-WP-PLAN-CAP-001` | `SPMS-WP-PLAN` | Must | 6 |
| `SPMS-WP-PLAN-CAP-002` | `SPMS-WP-PLAN` | Must | 6 |
| `SPMS-WP-PLAN-CAP-003` | `SPMS-WP-PLAN` | Must | 6 |
| `SPMS-WP-PLAN-CAP-004` | `SPMS-WP-PLAN` | Must | 6 |
| `SPMS-REQ-MGMT-CAP-001` | `SPMS-REQ-MGMT` | Must | 7 |
| `SPMS-REQ-MGMT-CAP-002` | `SPMS-REQ-MGMT` | Must | 7 |
| `SPMS-REQ-MGMT-CAP-003` | `SPMS-REQ-MGMT` | Must | 7 |
| `SPMS-REQ-MGMT-CAP-004` | `SPMS-REQ-MGMT` | Must | 7 |
| `SPMS-TEST-VV-CAP-001` | `SPMS-TEST-VV` | Must | 7 |
| `SPMS-TEST-VV-CAP-002` | `SPMS-TEST-VV` | Must | 7 |
| `SPMS-TEST-VV-CAP-003` | `SPMS-TEST-VV` | Must | 7 |
| `SPMS-TEST-VV-CAP-004` | `SPMS-TEST-VV` | Must | 7 |
| `SPMS-CICD-CAP-001` | `SPMS-CICD` | Must | 8 |
| `SPMS-CICD-CAP-002` | `SPMS-CICD` | Must | 8 |
| `SPMS-CICD-CAP-003` | `SPMS-CICD` | Must | 8 |
| `SPMS-CICD-CAP-004` | `SPMS-CICD` | Must | 8 |
| `SPMS-CFG-ASSET-CAP-001` | `SPMS-CFG-ASSET` | Must | 9 |
| `SPMS-CFG-ASSET-CAP-002` | `SPMS-CFG-ASSET` | Must | 9 |
| `SPMS-CFG-ASSET-CAP-003` | `SPMS-CFG-ASSET` | Must | 9 |
| `SPMS-CFG-ASSET-CAP-004` | `SPMS-CFG-ASSET` | Must | 9 |
| `SPMS-REL-DEP-CAP-001` | `SPMS-REL-DEP` | Must | 9 |
| `SPMS-REL-DEP-CAP-002` | `SPMS-REL-DEP` | Must | 9 |
| `SPMS-REL-DEP-CAP-003` | `SPMS-REL-DEP` | Must | 9 |
| `SPMS-REL-DEP-CAP-004` | `SPMS-REL-DEP` | Must | 9 |
| `SPMS-PROD-ASSUR-CAP-001` | `SPMS-PROD-ASSUR` | Must | 10 |
| `SPMS-PROD-ASSUR-CAP-002` | `SPMS-PROD-ASSUR` | Must | 10 |
| `SPMS-PROD-ASSUR-CAP-003` | `SPMS-PROD-ASSUR` | Must | 10 |
| `SPMS-PROD-ASSUR-CAP-004` | `SPMS-PROD-ASSUR` | Must | 10 |
| `SPMS-SEC-COMP-CAP-001` | `SPMS-SEC-COMP` | Must | 10 |
| `SPMS-SEC-COMP-CAP-002` | `SPMS-SEC-COMP` | Must | 10 |
| `SPMS-SEC-COMP-CAP-003` | `SPMS-SEC-COMP` | Must | 10 |
| `SPMS-SEC-COMP-CAP-004` | `SPMS-SEC-COMP` | Must | 10 |
| `SPMS-AUTO-AI-CAP-001` | `SPMS-AUTO-AI` | Must | 12 |
| `SPMS-AUTO-AI-CAP-002` | `SPMS-AUTO-AI` | Must | 12 |
| `SPMS-AUTO-AI-CAP-003` | `SPMS-AUTO-AI` | Must | 12 |
| `SPMS-AUTO-AI-CAP-004` | `SPMS-AUTO-AI` | Must | 12 |

**Conformance rule.** This §4 list and `SPMS-STD-SCALE §5` must agree. If they disagree, the
disagreement must be resolved before Phase 6 exit. Raise the discrepancy as a defect against
this document and `SPMS-STD-SCALE`.

# 5. Per-Phase Scope Locks

Once a phase begins (sprint planning has started for that phase's first epic), its capability
set is frozen. No new capability may be added to the phase's delivery scope without following
the deferral/injection process below.

**Phase scope lock process:**
1. At phase-boundary planning, the Programme Technical Authority signs off the capability set
   for the upcoming phase from this register.
2. Once signed off, the capability set is locked for that phase.
3. A new capability arising mid-phase is deferred to the backlog (see §6) unless the
   Programme Technical Authority grants an emergency injection waiver (Level 3 change,
   `SPMS-METHODOLOGY`), which requires written justification and scope impact assessment.
4. A capability that proves infeasible mid-phase is moved to the deferral register (§6) with
   the reason recorded. It does not carry over implicitly; it must be re-prioritised at the
   next phase boundary.
5. Re-estimation at each phase boundary from measured velocity (`RISK-010` mitigation in
   `SPMS-DELIVERY`) must include a review of §6 to promote or permanently defer items.

**Phase scope table (planned):**

| Phase | Planned capabilities in scope | Notes |
|---|---|---|
| 1 | PLAT-CORE-CAP-001–008 | Identity and record substrate |
| 2 | WF-GOV-CAP-001–008 | Workflow and governance engine |
| 3 | EVID-AUDIT-CAP-001–008; BASE-CCB-CAP-001–010; DATA-STORE-CAP-001–010 | Audit, baseline, and data layer |
| 4 | TRACE-GRAPH-CAP-001–008 | Graph substrate (INV-003 becomes active) |
| 5 | INT-EVENT-CAP-001–010; REPORT-ANALYTICS-CAP-001–008 | Event bus, reporting |
| 6 | WP-PLAN-CAP-001–008; ISS-CHG-CAP-001–008; DOC-KM-CAP-001–008 | First functional modules |
| 7 | REQ-MGMT-CAP-001–008; TEST-VV-CAP-001–008 | Requirements and V&V |
| 8 | CICD-CAP-001–008 | Build and CI/CD |
| 9 | REL-DEP-CAP-001–008; CFG-ASSET-CAP-001–008 | Release and configuration |
| 10 | SEC-COMP-CAP-001–008; PROD-ASSUR-CAP-001–008 | Security and assurance |
| 12 | AUTO-AI-CAP-001–008 | Automation and AI assistance |

# 6. Deferral Register

This table records capabilities that have been explicitly deferred. A capability is added here
when: (a) it is re-prioritised out of an in-scope tier for a phase, (b) it proves infeasible
mid-phase and is moved out, or (c) it is a Should/Could capability that has not yet been
scheduled. At each phase boundary the Programme Technical Authority reviews this register and
makes a recorded promote/defer/drop decision for each item.

**Should/Could capabilities not yet scheduled (initial population):**

| Capability ID | Component | Priority | Reason deferred | Target phase | Decision date |
|---|---|---|---|---|---|
| `SPMS-REPORT-ANALYTICS-CAP-005` | `SPMS-REPORT-ANALYTICS` | Should | Not required for minimal mode; advanced analytics deferred | TBD | 2026-06-15 |
| `SPMS-REPORT-ANALYTICS-CAP-006` | `SPMS-REPORT-ANALYTICS` | Should | Not required for minimal mode; advanced analytics deferred | TBD | 2026-06-15 |
| `SPMS-REPORT-ANALYTICS-CAP-007` | `SPMS-REPORT-ANALYTICS` | Should | Not required for minimal mode; advanced analytics deferred | TBD | 2026-06-15 |
| `SPMS-REPORT-ANALYTICS-CAP-008` | `SPMS-REPORT-ANALYTICS` | Should | Not required for minimal mode; advanced analytics deferred | TBD | 2026-06-15 |
| `SPMS-DOC-KM-CAP-005` | `SPMS-DOC-KM` | Should | Not required for minimal mode; enhanced KM features deferred | TBD | 2026-06-15 |
| `SPMS-DOC-KM-CAP-006` | `SPMS-DOC-KM` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-DOC-KM-CAP-007` | `SPMS-DOC-KM` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-DOC-KM-CAP-008` | `SPMS-DOC-KM` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-ISS-CHG-CAP-005` | `SPMS-ISS-CHG` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-ISS-CHG-CAP-006` | `SPMS-ISS-CHG` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-ISS-CHG-CAP-007` | `SPMS-ISS-CHG` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-ISS-CHG-CAP-008` | `SPMS-ISS-CHG` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-WP-PLAN-CAP-005` | `SPMS-WP-PLAN` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-WP-PLAN-CAP-006` | `SPMS-WP-PLAN` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-WP-PLAN-CAP-007` | `SPMS-WP-PLAN` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-WP-PLAN-CAP-008` | `SPMS-WP-PLAN` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REQ-MGMT-CAP-005` | `SPMS-REQ-MGMT` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REQ-MGMT-CAP-006` | `SPMS-REQ-MGMT` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REQ-MGMT-CAP-007` | `SPMS-REQ-MGMT` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REQ-MGMT-CAP-008` | `SPMS-REQ-MGMT` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-TEST-VV-CAP-005` | `SPMS-TEST-VV` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-TEST-VV-CAP-006` | `SPMS-TEST-VV` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-TEST-VV-CAP-007` | `SPMS-TEST-VV` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-TEST-VV-CAP-008` | `SPMS-TEST-VV` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CICD-CAP-005` | `SPMS-CICD` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CICD-CAP-006` | `SPMS-CICD` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CICD-CAP-007` | `SPMS-CICD` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CICD-CAP-008` | `SPMS-CICD` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CFG-ASSET-CAP-005` | `SPMS-CFG-ASSET` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CFG-ASSET-CAP-006` | `SPMS-CFG-ASSET` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CFG-ASSET-CAP-007` | `SPMS-CFG-ASSET` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-CFG-ASSET-CAP-008` | `SPMS-CFG-ASSET` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REL-DEP-CAP-005` | `SPMS-REL-DEP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REL-DEP-CAP-006` | `SPMS-REL-DEP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REL-DEP-CAP-007` | `SPMS-REL-DEP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-REL-DEP-CAP-008` | `SPMS-REL-DEP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-PROD-ASSUR-CAP-005` | `SPMS-PROD-ASSUR` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-PROD-ASSUR-CAP-006` | `SPMS-PROD-ASSUR` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-PROD-ASSUR-CAP-007` | `SPMS-PROD-ASSUR` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-PROD-ASSUR-CAP-008` | `SPMS-PROD-ASSUR` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-SEC-COMP-CAP-005` | `SPMS-SEC-COMP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-SEC-COMP-CAP-006` | `SPMS-SEC-COMP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-SEC-COMP-CAP-007` | `SPMS-SEC-COMP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-SEC-COMP-CAP-008` | `SPMS-SEC-COMP` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-AUTO-AI-CAP-005` | `SPMS-AUTO-AI` | Should | Not required for minimal mode; AI assistance enhancements deferred | TBD | 2026-06-15 |
| `SPMS-AUTO-AI-CAP-006` | `SPMS-AUTO-AI` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-AUTO-AI-CAP-007` | `SPMS-AUTO-AI` | Should | Not required for minimal mode | TBD | 2026-06-15 |
| `SPMS-AUTO-AI-CAP-008` | `SPMS-AUTO-AI` | Should | Not required for minimal mode | TBD | 2026-06-15 |

The Must-priority capabilities with `Required for minimal mode? = No` (BASE-CCB-CAP-006–010,
DATA-STORE-CAP-006–010, INT-EVENT-CAP-006–010) are Must-tier and therefore in scope for all
governance profiles per §3, but are not required in the Small/minimal deployment profile of
`SPMS-STD-SCALE §5`. They must be scheduled within Phase 3 (BASE-CCB, DATA-STORE) and Phase 5
(INT-EVENT) and are not deferred.

# 7. Governance, Approvals, Waivers, and Gates

Phase scope changes after lock require Level 3 approval (`SPMS-METHODOLOGY`) from the
Programme Technical Authority. Emergency injections are exceptions, not standard practice.

This register must be reviewed and signed off by the Programme Technical Authority at each
phase boundary. The sign-off is recorded as an `AuditEvent` of type `DocumentApproved` against
this register.

# 8. Evidence, Audit, and Historical Reconstruction

Changes to this register are controlled changes. Each change must be recorded as an `AuditEvent`
entry. The history of this register must support reconstruction of the approved capability set
at any past phase boundary.

# 9. Cross-References

| Document | Relationship |
|---|---|
| `SPMS-DELIVERY` | RISK-005 (scope creep mitigation); re-estimation at phase boundaries (RISK-010) |
| `SPMS-STD-SCALE §5` | Minimum Viable Governed Deployment; §4 of this register must agree with §5 |
| `SPMS-WF-GOV §8.1` | Governance profile definitions used in the §3 matrix |
| `SPMS-THINTHREAD` | Thin governed thread acceptance suite; covers the substrate Must-tier capabilities |
| `SPMS-INDEX §3` | Component list and phase assignments |
| `SPMS-METHODOLOGY` | Change control levels for scope lock waivers |
