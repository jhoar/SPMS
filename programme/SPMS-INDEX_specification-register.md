# SPMS Specification Register

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-INDEX |
| Component name | SPMS Specification Register |
| Component type | Programme register (controlling document) |
| Version | 1.0 |
| Status | Approved for reconciled set v1 |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |

---

# 1. Authoritative source statement

There is exactly one authoritative SPMS specification set: the **reconciled set v1**, listed in
section 3 and held in `specifications/`. The previously circulating numbered set
(`SPMS-SUB-001…010`, `SPMS-FUN-011…016`) is **superseded** and retained read-only in `_superseded/`
for reference and detail harvesting only. Where any document conflicts with a reconciled-set
specification, the reconciled-set specification governs. Implementation, estimation, and review
draw from the reconciled set alone.

# 2. How the corpus was reconciled

The corpus previously held two overlapping families covering the same platform: a named set
(complete on functional modules, lighter on substrate) and a numbered set (rich on substrate,
missing the six core operational modules). Reconciliation kept the named set as the canonical
module/functional layer, promoted the three substrate concerns that had no named owner into
first-class specifications, normalized identifiers and document control across all of them, and
superseded the numbered set. See `SPMS-METHODOLOGY` for the delivery-methodology reconciliation and
`SPMS-DOMAIN-MODEL` for the single record model and relationship registry.

# 3. Canonical specification set (19 components)

| # | Spec ID | Title | Owner | Supersedes | Phase |
|---|---|---|---|---|---|
| 1 | `SPMS-PLAT-CORE` | Platform Core | Platform Architecture Lead | SUB-001; SUB-002 (record model); SUB-010 (admin/ops) | 1 |
| 2 | `SPMS-WF-GOV` | Workflow & Governance Core | Governance Engineering Lead | SUB-003 | 2 |
| 3 | `SPMS-EVID-AUDIT` | Evidence & Audit Core | Assurance Data Lead | SUB-005 | 3 |
| 4 | `SPMS-BASE-CCB` | Baseline, Version & Change-Control Engine | Assurance Data Lead | SUB-006 | 3 |
| 5 | `SPMS-DATA-STORE` | Data Persistence Layer | Platform Architecture Lead | SUB-009 | 3 |
| 6 | `SPMS-TRACE-GRAPH` | Traceability Graph Core | Traceability & Data Lead | SUB-004 | 4 |
| 7 | `SPMS-INT-EVENT` | Integration & Event Framework | Engineering Integration Lead | SUB-008 | 5 |
| 8 | `SPMS-REPORT-ANALYTICS` | Reporting & Analytics | Analytics Lead | FUN-015; SUB-007 | 5, 11 |
| 9 | `SPMS-WP-PLAN` | Planning & Work Packages | Delivery Modules Lead | — | 6 |
| 10 | `SPMS-ISS-CHG` | Issue & Change Management | Delivery Modules Lead | — | 6 |
| 11 | `SPMS-DOC-KM` | Document & Knowledge Management | Delivery Modules Lead | — | 6 |
| 12 | `SPMS-REQ-MGMT` | Requirements Management | Requirements & V&V Lead | — | 7 |
| 13 | `SPMS-TEST-VV` | Test/V&V Management | Requirements & V&V Lead | — | 7 |
| 14 | `SPMS-CICD` | Build & CI/CD Management | Engineering Integration Lead | — | 8 |
| 15 | `SPMS-REL-DEP` | Release & Deployment Management | Release Engineering Lead | FUN-011 | 9 |
| 16 | `SPMS-CFG-ASSET` | Configuration & Asset Management | Release Engineering Lead | FUN-012 | 9 |
| 17 | `SPMS-SEC-COMP` | Security & Compliance Management | Security & Compliance Lead | FUN-013; SUB-010 (security) | 10 |
| 18 | `SPMS-PROD-ASSUR` | Product Assurance | Product Assurance Lead | FUN-014 | 10 |
| 19 | `SPMS-AUTO-AI` | Automation & AI Assistance | AI Assurance Lead | FUN-016 | 12 |

# 4. Programme standards and registers

| Spec ID | Title | Purpose |
|---|---|---|
| `SPMS-INDEX` | Specification Register | This document; authoritative source statement |
| `SPMS-STD-ID` | Identifier & Naming Standard | Global identifier scheme |
| `SPMS-STD-SCALE` | Scale Envelope Standard | Quantified scale behind NFR targets; §5 defines Minimum Viable Governed Deployment |
| `SPMS-DOMAIN-MODEL` | Canonical Domain Model & Relationship Registry | Single record model, link types, and §7 canonical entity schemas |
| `SPMS-METHODOLOGY` | Delivery Methodology Reconciliation Note | Resolves planning-document conflict |
| `SPMS-DELIVERY` | Delivery Plan & Risk Register | Effort, staffing, timeline, risk, thin governed thread |
| `SPMS-STD-EVENT` | Event & Outbox Model Standard | Transactional outbox pattern, event envelope schema, projection consumption contract, idempotency, retry/dead-letter, and rebuild protocol |
| `SPMS-STD-SEC` | Security Architecture Standard | Tenant isolation model, ABAC/RBAC evaluation order, field-level security, service identity, secret-reference handling, audit log tamper resistance, export-control enforcement, and AI retrieval permission boundaries |
| `SPMS-STD-MIG` | Migration & Import Strategy Standard | Shared import pipeline (parse/validate/map/dry-run/commit), ID mapping table, reconciliation, and rollback framework for all module importers |
| `SPMS-STD-MODULE` | Shared Module Requirements Standard | Canonical user types, role model, common UI patterns, shared NFR defaults, shared audit/import/export/security requirements; authoritative source for boilerplate common to all functional module specs |
| `SPMS-STD-INVARIANTS` | Substrate Correctness Invariants Standard | Seven formal substrate invariants (INV-001–007) with property-based verification methods, CI phase gates, and ownership assignments; structural mitigation for RISK-001 and RISK-004 |
| `SPMS-STD-CONFIG` | Configuration Governance Standard | Configuration taxonomy (Fixed / Canonical-constrained / Free), tenant-divergence consistency guardrails, configuration change governance, and configuration baselining; structural mitigation for RISK-011 |

# 4a. Programme documents

| Doc ID | Title | Purpose |
|---|---|---|
| `SPMS-THINTHREAD` | Thin Governed Thread Acceptance Suite | Formalises the thin governed thread as 10 executable acceptance test scenarios (TGT-001–TGT-010); invariant smoke test for every phase exit from Phase 2 onward |
| `SPMS-UX` | UI/UX Information Architecture | Navigation model, workspace hierarchy, queue semantics, global search, record detail layout, graph exploration UX, dashboard strategy, and admin configuration UX |
| `SPMS-SCOPE` | Scope & Prioritisation Register | Central rollup of all 158 capability priorities across 19 components; governance-profile × capability-inclusion matrix; per-phase scope locks; deferral register; structural mitigation for RISK-005 |

# 5. Dependency overview

`SPMS-DATA-STORE` underpins everything. `SPMS-PLAT-CORE` provides identity and the record model to
all components. `SPMS-WF-GOV`, `SPMS-EVID-AUDIT`, `SPMS-BASE-CCB`, `SPMS-TRACE-GRAPH`, and
`SPMS-INT-EVENT` are the substrate every functional module consumes. Functional modules
(`WP-PLAN`, `ISS-CHG`, `DOC-KM`, `REQ-MGMT`, `TEST-VV`, `CICD`, `REL-DEP`, `CFG-ASSET`, `SEC-COMP`,
`PROD-ASSUR`) consume the substrate and never reimplement it. `REPORT-ANALYTICS` reads from all;
`AUTO-AI` reads from all and writes only proposals subject to human approval. The build order in the
Phase column matches the Phase Implementation Plan.

# 6. Status

All 19 component specifications are at Version 0.2, Status "Draft — Authoritative (reconciled set
v1)". They pass the specification linter (`tools/spec_lint.py`). Promotion to Version 1.0 / Approved
requires named reviewers and approvers to sign off and the detail-harvest backlog
(`DETAIL-HARVEST-BACKLOG`) to be cleared or explicitly deferred per item.
