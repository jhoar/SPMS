# Shared Module Requirements Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-MODULE |
| Component name | Shared Module Requirements Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | All functional module specifications |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

The 19 component specifications in the reconciled set v1 each include sections on user types,
role models, common UI patterns, NFR defaults, audit requirements, import/export, and security
requirements. This content is substantively identical across all functional modules.

This standard is the **single authoritative source** for that shared content. Module
specifications at v0.2 include these sections inline for completeness; from v0.3 onward, module
specs may replace identical inline sections with a reference to this standard, making each spec
shorter and more specific to its domain.

Changes to shared requirements are made here and propagate to all modules. A change to a
shared requirement is a Level 2 controlled change to this document.

# 2. Canonical User Types

Every functional module supports the following user types. This table is the single authoritative
definition; module spec §3.1 tables are derived from it.

| User type | Description | Typical permissions |
|---|---|---|
| Administrator | Configures the component and its policies. | Configure, administer, monitor, migrate. |
| Owner | Accountable for records or configuration in this component. | Create, review, approve where authorised, close. |
| Contributor | Creates or modifies records. | Create, edit drafts, comment, attach evidence. |
| Reviewer | Reviews records, evidence, or changes. | Review, comment, request changes, recommend approval. |
| Approver | Provides formal approval. | Approve, reject, conditionally approve, request rework. |
| Viewer | Reads information. | Read permitted records, dashboards, reports. |
| Auditor | Reviews historical state and evidence. | Read audit trails, exports, baselines, evidence packages. |
| External collaborator | Customer, supplier, partner, regulator, or auditor. | Restricted review / comment / approval / export as configured. |
| Automation actor | System, integration, agent, bot, or scheduled job. | API actions under scoped service identity (`SPMS-STD-SEC` §5). |

# 3. Canonical Role Model

Every functional module derives its role model from the following canonical roles. Module specs
may add module-specific roles (e.g., "Release Manager" in `SPMS-REL-DEP`) but must not
redefine these base roles.

| Role | Responsibilities | Authority | Separation-of-duty constraints |
|---|---|---|---|
| Component administrator | Configure schemas, workflows, integrations, retention, and views. | Administrative authority within assigned tenant/project. | Cannot self-approve controlled records unless explicitly allowed in Lightweight profile. |
| Record owner | Maintain correctness, completeness, and timely closure. | Owns records; may submit for review. | Cannot independently approve own controlled changes in Controlled/Critical profiles. |
| Technical reviewer | Assess technical correctness and completeness. | Recommend approval or request changes. | Must be independent where configured. |
| Governance approver | Make formal gate, baseline, waiver, or acceptance decisions. | Approve/reject controlled records and gates. | Cannot be requester for the same approval in Controlled/Critical profiles. |
| Auditor | Inspect evidence, history, and compliance. | Read-only access to audit scope. | Cannot modify audited records. |
| External collaborator | Participate in designated review or acceptance activities. | Restricted as configured; may not approve unilaterally. | Cannot approve records affecting own deliverables. |
| Automation actor | Execute configured rules, imports, or AI functions. | API access under service identity; scoped to assigned capabilities. | Cannot approve controlled records; all actions produce audit events. |

# 4. Common UI Patterns

All SPMS functional modules share the UI structural patterns defined in `SPMS-UX`. The following
table lists the specific UI component patterns that every module must instantiate.

| Pattern | Description | Reference |
|---|---|---|
| Record list view | Filterable, sortable table of records; bulk-action toolbar; column configurability; pagination or virtual scroll | `SPMS-UX` §3 |
| Record detail view | Header strip (ID, title, state, owner, classification, actions); tabbed body (Details, Links, Evidence, History, Activity) | `SPMS-UX` §6 |
| Bulk import wizard | 5-stage import flow mirroring `SPMS-STD-MIG` pipeline: Upload → Validate → Map → Dry-run review → Confirm | `SPMS-STD-MIG` §3 |
| Export dialog | Format selector (JSON, CSV); field selector; classification warning; approval gate trigger for restricted exports | `SPMS-STD-SEC` §8 |
| Linked-record picker | Search-as-you-type picker for creating trace links; shows record type, id, title, state; grouped by link type | `SPMS-DOMAIN-MODEL` §5 |
| Evidence attachment panel | List of attached evidence with type, uploaded-by, date, status; upload button; expiry warning | `SPMS-EVID-AUDIT` |
| Audit trail viewer | Chronological, immutable event log for the record; filterable by event type and actor; tamper-indicator if hash chain fails | `SPMS-STD-SEC` §7 |
| Workflow status widget | Current state badge; next available transitions; gate status; SLA countdown; pending approvals | `SPMS-WF-GOV` |

# 5. Shared NFR Defaults

Unless a module specification explicitly overrides a target, these defaults apply at the
Standard scale profile (`SPMS-STD-SCALE` §3).

| Requirement | Default target | Source |
|---|---|---|
| Record list / detail view latency | P95 < 2 s, P99 < 4 s | `NFR-PERF-001` |
| Search query latency | P95 < 2 s | `NFR-PERF-002` |
| Import throughput | ≥ 10,000 records/hour sustained | `NFR-PERF-005` |
| Dashboard rendering | P95 < 3 s (≤ 12 widgets, pre-aggregated) | `NFR-PERF-008` |
| Service availability | ≥ 99.5% (standard); ≥ 99.9% (critical deployments) | `NFR-AVAIL-001` |
| Recovery point objective | ≤ 15 minutes | `NFR-DR-001` |
| Recovery time objective | ≤ 4 h (standard); ≤ 1 h (critical) | `NFR-DR-001` |

Module specifications must reference `SPMS-STD-SCALE` and these identifiers rather than
restating the numeric targets, so that targets remain centrally governed.

# 6. Shared Audit Requirements

Every functional module must emit `AuditEvent` records (`SPMS-DOMAIN-MODEL` §7.4) for the
following operations as a minimum:

| Operation | Event type |
|---|---|
| Record created | `RecordCreated` |
| Record field(s) edited | `RecordUpdated` |
| Lifecycle state changed | `StateChanged` |
| Approval decision made | `ApprovalCompleted` |
| Evidence attached or updated | `EvidenceAttached` / `EvidenceUpdated` |
| Evidence expired or revoked | `EvidenceExpired` / `EvidenceRevoked` |
| Record included in or removed from a baseline | `BaselineMembershipChanged` |
| Trace link created or retracted | `LinkCreated` / `LinkRetracted` |
| Bulk import committed or rolled back | `ImportCommitted` / `ImportRolledBack` |
| Record exported | `RecordExported` |
| Permission-sensitive access (read of restricted record) | `RestrictedRecordAccessed` |

Module specifications may add module-specific event types; they must not omit any event type
from this mandatory set.

# 7. Shared Import/Export Requirements

## 7.1 Import

All functional modules that accept external data must implement the 5-stage import pipeline
defined in `SPMS-STD-MIG` §3. There are no exceptions. Module-specific importer requirements
(supported source formats, field mappings, deduplication keys) are defined in the module
specification and supplemented by this standard's pipeline.

## 7.2 Export

Every functional module must support the following export capabilities:

| Format | Required | Notes |
|---|---|---|
| JSON | Yes | Full record export with all fields; classification-filtered per actor |
| CSV | Yes | Flat tabular export of core fields; useful for spreadsheet tooling |
| API-driven (REST/GraphQL) | Yes | Paginated, permission-filtered; consumed by integrations |

Large exports (> 10,000 records) must be generated asynchronously and delivered via a
download link or notification; they must not block the API call.

Export of `restricted` records requires explicit `export` permission (`SPMS-STD-SEC` §8).

# 8. Shared Security Requirements

Every functional module must comply with `SPMS-STD-SEC` in full. The following table summarises
the minimum per-module security obligations:

| Requirement | Standard reference |
|---|---|
| Enforce `tenant_id` isolation on all record reads and writes | `SPMS-STD-SEC` §2 |
| Apply the 6-layer ABAC/RBAC evaluation order on every request | `SPMS-STD-SEC` §3 |
| Redact field content for actors below the record's classification level | `SPMS-STD-SEC` §4.1 |
| Refuse direct writes to write-protected fields (`lifecycle_state`, `version`, etc.) | `SPMS-STD-SEC` §4.2 |
| Filter fields before serialising any export | `SPMS-STD-SEC` §4.3 |
| Use service tokens (not user tokens) for inter-service calls | `SPMS-STD-SEC` §5.1 |
| Produce `AuditEvent` with `actor_type: automation` for all automation actions | `SPMS-STD-SEC` §5.2 |
| Never store raw secret values | `SPMS-STD-SEC` §6.1 |
| Produce `RecordExported` `AuditEvent` on every export | `SPMS-STD-SEC` §8.3 |
