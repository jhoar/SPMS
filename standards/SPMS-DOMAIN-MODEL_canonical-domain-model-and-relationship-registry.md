# Canonical Domain Model & Relationship Registry

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-DOMAIN-MODEL |
| Component name | Canonical Domain Model & Relationship Registry |
| Component type | Programme standard (normative) |
| Version | 1.0 |
| Status | Approved for reconciled set v1 |
| Owner | Platform Architecture Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |
| Applies to | Every component specification |

---

# 1. Purpose

Two independently authored specification families each restated the core record model and the link
types (one called it the "common object model", the other the "common record model"), which is how
the corpus drifted into two versions of the same platform. This document is the single normative
source for the shared record model, lifecycle states, and relationship types. Component
specifications **reference** these definitions; they do not redefine them. If a component needs a
field, state, or link type that is not here, the change is made here first and then consumed.

# 2. Single ownership of shared concerns

Each cross-cutting concern has exactly one owning component. No other component may implement a
private version of it.

| Shared concern | Sole owning component |
|---|---|
| Tenancy, identity, permissions, common record model, metadata, classification, admin | `SPMS-PLAT-CORE` |
| Lifecycle/state machine, approvals, gates, waivers, delegation, SLA, separation of duties | `SPMS-WF-GOV` |
| Relationship/trace graph, coverage, impact, suspect links, topology | `SPMS-TRACE-GRAPH` |
| Evidence registry, immutable audit log, evidence integrity | `SPMS-EVID-AUDIT` |
| Baselines, versioning, change requests, change control, historical reconstruction | `SPMS-BASE-CCB` |
| Event bus, domain-event contracts, webhooks, external integration | `SPMS-INT-EVENT` |
| Object storage, relational store, graph projection, search index, metrics store | `SPMS-DATA-STORE` |
| Search, saved views, dashboards, reporting, metrics model | `SPMS-REPORT-ANALYTICS` |

This table resolves the previous overlaps where, for example, the event bus was described across
five different specifications and baseline/version/change-control had no owner at all.

# 3. Common Record Model

Every controlled record in the system extends the Common Record Model, owned by `SPMS-PLAT-CORE`.

| Field | Type | Notes |
|---|---|---|
| `id` | identifier | Per `SPMS-STD-ID` §4; stable for record life |
| `component` | code | Owning component code |
| `record_type` | enum | Component-defined within its namespace |
| `tenant_id` | identifier | Tenant isolation boundary; mandatory |
| `project_id` | identifier | Nullable for tenant-level records |
| `title` | string | Human label |
| `lifecycle_state` | enum | From §4 |
| `classification` | enum | e.g. public / internal / confidential / restricted |
| `owner_id` | identifier | Accountable party |
| `metadata` | map | Validated against the record type's metadata schema |
| `version` | integer | Optimistic lock; incremented by controlled update |
| `baseline_refs` | list | Baselines this version participates in (`SPMS-BASE-CCB`) |
| `created_at` / `created_by` | timestamp / id | Immutable |
| `updated_at` / `updated_by` | timestamp / id | Last controlled change |
| `superseded_by` | identifier | Set on supersession; never deletes history |

Records never hard-delete; they transition to `retired` or `superseded`. All meaningful changes
emit an audit event (`SPMS-EVID-AUDIT`) and a domain event (`SPMS-INT-EVENT`).

# 4. Canonical lifecycle states

Component lifecycles are configured in `SPMS-WF-GOV` but must map onto this canonical state set so
that cross-module reporting and reconstruction are consistent.

`draft → in_review → approved → baselined → in_change → verified → accepted → retired`
with side states `rejected`, `superseded`, `waived`, and `reopened`.

Not every component uses every state; each component declares its subset and the transitions it
permits. Transitions are policy-driven, never hardcoded in a module.

# 5. Relationship registry

This is the authoritative set of trace link types. Link type identifiers follow
`SPMS-TRACE-GRAPH-REL-<NNN>`. Links are bidirectional and carry provenance, creation actor, and
suspect state (`SPMS-TRACE-GRAPH`).

| Link id | Name | Source → Target | Cardinality | Required coverage |
|---|---|---|---|---|
| `SPMS-TRACE-GRAPH-REL-001` | derives-from | Requirement → Need/Decision/Requirement | N:N | For derived requirements |
| `SPMS-TRACE-GRAPH-REL-002` | decomposes-to | Work package → Task | 1:N | For decomposed work |
| `SPMS-TRACE-GRAPH-REL-003` | implements | Work/Build/Code → Requirement/Decision | N:N | For delivery coverage |
| `SPMS-TRACE-GRAPH-REL-004` | verifies | Test/Evidence → Requirement | N:N | For verified requirements |
| `SPMS-TRACE-GRAPH-REL-005` | validates | Scenario → Stakeholder need | N:N | For validation |
| `SPMS-TRACE-GRAPH-REL-006` | blocks | Task → Release/Task | N:N | Optional |
| `SPMS-TRACE-GRAPH-REL-007` | depends-on | Service → API/Database/Service | N:N | For topology |
| `SPMS-TRACE-GRAPH-REL-008` | deployed-to | Component → Environment | N:N | For deployments |
| `SPMS-TRACE-GRAPH-REL-009` | affects | Vulnerability → Asset | N:N | For security impact |
| `SPMS-TRACE-GRAPH-REL-010` | mitigates | Control → Risk | N:N | For risk treatment |
| `SPMS-TRACE-GRAPH-REL-011` | included-in | Requirement/Issue → Release | N:N | For release scope |
| `SPMS-TRACE-GRAPH-REL-012` | evidenced-by | Verification → Test result/Evidence | N:N | For evidence-based acceptance |
| `SPMS-TRACE-GRAPH-REL-013` | approved-by | Baseline/Record → Authority | N:N | For controlled approvals |
| `SPMS-TRACE-GRAPH-REL-014` | produced-by | Evidence/Artifact/Metric → Job/Pipeline/Automation | N:N | For provenance |
| `SPMS-TRACE-GRAPH-REL-015` | supersedes | Record → Record | 1:N | On controlled replacement |

New link types are added here with the next free identifier; they are never invented inside a
component specification.

# 6. Conformance

The linter checks that component specifications reference (not redefine) the record model, use only
registered link types in their "Required Trace Links" sections, and map their lifecycle states to
§4. Adding a field, state, or link type is a Level 2 controlled change to this document.
