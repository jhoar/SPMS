# Scale Envelope Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-SCALE |
| Component name | Scale Envelope Standard |
| Component type | Programme standard |
| Version | 1.0 |
| Status | Approved for reconciled set v1 |
| Owner | Platform Architecture Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |
| Applies to | Every specification's Non-Functional Requirements section |

---

# 1. Purpose

The component specifications state performance targets such as "P95 under 2 seconds for standard
record views **at target scale**" but the target scale was never quantified, so the targets were
not testable. This standard defines the scale the targets are measured against. Every NFR in every
specification is now read as "<target> at the **Standard** profile unless the specification names a
different profile." Performance, load, and capacity tests in the implementation plan are written
against these numbers.

# 2. Deployment profiles

| Dimension | Small (single team) | Standard (default) | Large (portfolio) |
|---|---|---|---|
| Tenants | 1 | 1–5 | up to 50 |
| Projects (per tenant) | up to 10 | up to 200 | up to 2,000 |
| Active users | up to 50 | up to 2,000 | up to 20,000 |
| Concurrent users (peak) | 20 | 500 | 5,000 |
| Controlled records (total) | up to 100,000 | up to 5,000,000 | up to 100,000,000 |
| Trace relationships (total) | up to 250,000 | up to 20,000,000 | up to 500,000,000 |
| Evidence objects | up to 200,000 | up to 10,000,000 | up to 250,000,000 |
| Evidence volume | up to 1 TB | up to 50 TB | up to 2 PB |
| Domain events / day | up to 100,000 | up to 10,000,000 | up to 200,000,000 |
| Integrations (Git/CI/scanner/etc.) | up to 10 | up to 100 | up to 1,000 |
| Baselines retained | up to 1,000 | up to 100,000 | up to 2,000,000 |

The system must run the Small profile without requiring portfolio structures, partitioning, or
dedicated workers (this preserves the "usable by a single team" requirement). Standard and Large
are reached through configuration, indexing, graph projection, worker scaling, and partitioning —
not through code forks.

# 3. Performance targets bound to the Standard profile

These restate the targets already present in the specifications and bind them to section 2. Unless
a specification states otherwise, these apply at the **Standard** profile under peak concurrency.

| Identifier | Target |
|---|---|
| `NFR-PERF-001` | Standard record view: P95 < 2 s, P99 < 4 s |
| `NFR-PERF-002` | Indexed search query: P95 < 2 s |
| `NFR-PERF-003` | Bounded impact / traceability query (depth ≤ 5, ≤ 10,000 nodes): P95 < 5 s |
| `NFR-PERF-004` | Unbounded graph analytics (matrix, coverage rebuild): asynchronous, P95 < 5 min |
| `NFR-PERF-005` | Record import with validation: ≥ 10,000 records/hour sustained |
| `NFR-PERF-006` | Domain event end-to-end processing: P95 < 60 s |
| `NFR-PERF-007` | Evidence upload (≤ 100 MB object): P95 < 10 s incl. hashing |
| `NFR-PERF-008` | Dashboard with ≤ 12 widgets: P95 < 3 s on pre-aggregated metrics |
| `NFR-AVAIL-001` | Availability: ≥ 99.5% standard deployments; ≥ 99.9% critical deployments |
| `NFR-DR-001` | RPO ≤ 15 min; RTO ≤ 4 h (Standard); RTO ≤ 1 h (critical) |

# 4. Use in testing

The performance and resilience test levels in the phase implementation plan and the agile
validation approach run against the Standard profile by default, with a scheduled Large-profile
soak test per release candidate for components on the critical path (graph traversal, search,
evidence store, event bus). Targets that cannot be met at a profile are recorded as accepted
risk with a remediation plan, never silently relaxed.

# 5. Minimum Viable Governed Deployment

The Small profile (§2) defines hardware and capacity constraints. This section defines the
minimum **functional scope** for the smallest useful production deployment within that profile:
one team, one project, with end-to-end governed record control.

## 5.1 Required substrate components

All of the following must be present and operational before the deployment is considered governed:

| Component | Role |
|---|---|
| `SPMS-PLAT-CORE` | Tenant, project, identity, permissions, common record model |
| `SPMS-WF-GOV` | Lifecycle, approvals, gates, waivers, SLA |
| `SPMS-EVID-AUDIT` | Evidence registry, immutable audit log |
| `SPMS-BASE-CCB` | Baselines, versioning, change control |
| `SPMS-TRACE-GRAPH` | Relationship graph, coverage, suspect links |
| `SPMS-INT-EVENT` | Event bus, outbox relay, domain-event contracts |
| `SPMS-DATA-STORE` | Relational store, object storage, graph and search projections |

## 5.2 Required functional modules

The minimum governed deployment must include the following functional modules (or enough of each
to satisfy the record types in §5.3):

| Module | Minimum scope |
|---|---|
| `SPMS-ISS-CHG` | Issue/change record lifecycle |
| `SPMS-DOC-KM` | Document record lifecycle |
| `SPMS-REQ-MGMT` | Requirement record lifecycle |
| `SPMS-TEST-VV` | Test case and verification record lifecycle |
| `SPMS-REL-DEP` | Release record with evidence and baseline |

## 5.3 Required record types

The deployment must support creation, workflow, approval, evidence attachment, baselining,
trace linking, and audit reconstruction for each of the following record types:

- Controlled item (generic, used for thin governed thread validation)
- Issue / change record
- Document
- Requirement
- Test case / verification record
- Evidence record
- Baseline
- Trace link
- Release record
- Audit event

## 5.4 Required end-to-end capability

The deployment must pass all 10 scenarios in the Thin Governed Thread Acceptance Suite
(`SPMS-THINTHREAD`) end to end before it may be declared a governed production deployment.

## 5.5 Optional components (may be deferred)

The following components are not required for the minimum governed deployment and may be added
incrementally:

| Component | Typical phase |
|---|---|
| `SPMS-WP-PLAN` | Phase 6 |
| `SPMS-CICD` | Phase 8 |
| `SPMS-CFG-ASSET` | Phase 9 |
| `SPMS-SEC-COMP` | Phase 10 |
| `SPMS-PROD-ASSUR` | Phase 10 |
| `SPMS-REPORT-ANALYTICS` | Phase 5/11 (basic export from DATA-STORE sufficient initially) |
| `SPMS-AUTO-AI` | Phase 12 |

## 5.6 Governance profile constraint

The minimum deployment may operate at the **Lightweight** or **Low-risk bulk** governance profiles
(SPMS-WF-GOV §8.1). The **Controlled** and **Critical** profiles require the full functional module
set to be present before activation, as their gate and evidence requirements reference capabilities
across all modules.

The performance and resilience test levels in the phase implementation plan and the agile
validation approach run against the Standard profile by default, with a scheduled Large-profile
soak test per release candidate for components on the critical path (graph traversal, search,
evidence store, event bus). Targets that cannot be met at a profile are recorded as accepted
risk with a remediation plan, never silently relaxed.
