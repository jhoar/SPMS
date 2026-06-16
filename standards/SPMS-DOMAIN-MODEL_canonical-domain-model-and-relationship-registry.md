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
| Last updated | 2026-06-16 |
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
| `SPMS-TRACE-GRAPH-REL-016` | governed-by | Record → Workflow/Policy/Gate | N:N | For controlled-process binding |
| `SPMS-TRACE-GRAPH-REL-017` | hosted-on | Configuration item/Service → Asset/Environment | N:N | For physical/host topology |
| `SPMS-TRACE-GRAPH-REL-018` | connected-to | Configuration item/Interface → Configuration item | N:N | For network/interface topology |
| `SPMS-TRACE-GRAPH-REL-019` | backed-up-by | Configuration item/Data store → Backup/Job | N:N | For recoverability topology |
| `SPMS-TRACE-GRAPH-REL-020` | monitored-by | Configuration item/Service → Observability signal | N:N | For operational coverage |

New link types are added here with the next free identifier; they are never invented inside a
component specification. Link types REL-016…020 were added by the detail-harvest backlog
(`DETAIL-HARVEST-BACKLOG` items H-01/H-02): `governed-by` supports release change-control and
workflow binding; the topology links (`hosted-on`, `connected-to`, `backed-up-by`, `monitored-by`)
support configuration/asset topology that was previously over-loaded onto `depends-on`. Components
that only need a coarse dependency may continue to use `depends-on (REL-007)`.

# 6. Conformance

The linter checks that component specifications reference (not redefine) the record model, use only
registered link types in their "Required Trace Links" sections, and map their lifecycle states to
§4. Adding a field, state, or link type is a Level 2 controlled change to this document.

---

# 7. Canonical Entity Schemas

Concrete field-by-field schemas for the canonical entities. Entities that are controlled records
extend `Record` (§7.1) and inherit all Common Record Model fields (§3); their tables list only
additional fields. Entities that are not controlled records (e.g. `AuditEvent`, `IntegrationEvent`,
`TraceLink`) define their full field sets independently.

All schemas are owned by the component listed in §2. Changes to any schema below are Level 2
controlled changes to this document.

## 7.1 Record (shared — realises the Common Record Model)

This is the concrete storage realisation of §3. All module record types (Requirement, Issue,
Document, etc.) are instances of `Record` with a component-specific `record_type` value and
additional fields in `metadata`.

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `id` | string (SPMS-STD-ID format) | Yes | Immutable; globally unique within tenant | Stable for record lifetime |
| `component` | string | Yes | Must match a registered component code | e.g. `SPMS-REQ-MGMT` |
| `record_type` | string | Yes | Component-defined enum | e.g. `requirement`, `issue`, `document` |
| `tenant_id` | string | Yes | Must match authenticated session tenant | Tenant isolation boundary |
| `project_id` | string | No | Null for tenant-level records | Required for project-scoped records |
| `title` | string | Yes | 1–500 characters | Human label |
| `lifecycle_state` | string | Yes | Must be a value from §4 canonical state set | Transition rules from SPMS-WF-GOV |
| `classification` | string | Yes | One of: `public`, `internal`, `confidential`, `restricted` | Governs access and export |
| `owner_id` | string | Yes | Must resolve to an active User or Role | Accountable party |
| `metadata` | object | No | Validated against `record_type` metadata schema | Extensible per module |
| `version` | integer | Yes | Starts at 1; incremented on each controlled update | Optimistic concurrency lock |
| `baseline_refs` | array of strings | No | Each entry is a Baseline `id` | Populated by SPMS-BASE-CCB |
| `created_at` | timestamp (ISO 8601) | Yes | Immutable; set on creation | — |
| `created_by` | string | Yes | Immutable; actor id at creation | — |
| `updated_at` | timestamp (ISO 8601) | Yes | Updated on each controlled change | — |
| `updated_by` | string | Yes | Actor id of last controlled change | — |
| `superseded_by` | string | No | Id of superseding record; set on supersession | Never deletes history |

---

## 7.2 Platform Core entities (SPMS-PLAT-CORE)

### Tenant

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `tenant_id` | string | Yes | Immutable; globally unique | Primary isolation boundary |
| `name` | string | Yes | 1–200 characters; unique across platform | Display name |
| `slug` | string | Yes | Lowercase alphanumeric + hyphens; unique; immutable after creation | URL-safe identifier |
| `status` | string | Yes | One of: `active`, `suspended`, `archived` | Platform-level lifecycle |
| `classification_policy` | string | Yes | Default classification for new records in this tenant | Overridable per project |
| `governance_profile` | string | Yes | One of: `lightweight`, `low-risk-bulk`, `standard`, `controlled`, `critical` | Default for new projects |
| `secret_manager_ref` | string | No | `secret:<provider>:<name>:<version>` format (SPMS-STD-SEC §6) | External secret manager config |
| `sso_config_ref` | string | No | Reference to SSO/OIDC/SAML configuration | From integration config |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable; platform administrator id | — |
| `updated_at` | timestamp | Yes | — | — |
| `updated_by` | string | Yes | — | — |

### Project

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `project_id` | string | Yes | Immutable; unique within tenant | — |
| `tenant_id` | string | Yes | Foreign key to Tenant | — |
| `name` | string | Yes | 1–200 characters; unique within tenant | — |
| `slug` | string | Yes | Unique within tenant; immutable after creation | — |
| `status` | string | Yes | One of: `active`, `archived`, `suspended` | — |
| `governance_profile` | string | Yes | Inherits from Tenant; overridable | — |
| `enabled_modules` | array of strings | Yes | Subset of registered component codes | Controls which module UIs/APIs are active |
| `product_id` | string | No | Foreign key to Product (optional grouping) | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |
| `updated_at` | timestamp | Yes | — | — |
| `updated_by` | string | Yes | — | — |

### Product

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `product_id` | string | Yes | Immutable; unique within tenant | Optional portfolio grouping |
| `tenant_id` | string | Yes | — | — |
| `name` | string | Yes | 1–200 characters | — |
| `status` | string | Yes | One of: `active`, `archived` | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |

### Team

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `team_id` | string | Yes | Immutable; unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `name` | string | Yes | 1–200 characters | — |
| `project_ids` | array of strings | No | Projects this team is assigned to | — |
| `status` | string | Yes | One of: `active`, `archived` | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |

### User

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `user_id` | string | Yes | Immutable; unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `identity_ref` | string | Yes | External identity provider subject identifier | SSO / OIDC sub claim |
| `display_name` | string | Yes | 1–200 characters | — |
| `email` | string | Yes | Valid email; unique within tenant | — |
| `status` | string | Yes | One of: `active`, `suspended`, `archived` | — |
| `classification_clearance` | string | Yes | One of: `public`, `internal`, `confidential`, `restricted` | Highest classification this user may access |
| `team_ids` | array of strings | No | Teams this user belongs to | — |
| `is_service_account` | boolean | Yes | Default false; true for automation actors | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |
| `updated_at` | timestamp | Yes | — | — |
| `updated_by` | string | Yes | — | — |

### Role

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `role_id` | string | Yes | Unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `name` | string | Yes | One of canonical role names (SPMS-STD-MODULE §2) or custom | — |
| `scope` | string | Yes | One of: `tenant`, `project`, `component` | Scope at which this role is assigned |
| `is_system` | boolean | Yes | True for built-in roles; false for custom | System roles cannot be deleted |
| `created_at` | timestamp | Yes | Immutable | — |

### Permission

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `permission_id` | string | Yes | Unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `principal_id` | string | Yes | User id, Team id, or Role id | Subject of the permission grant |
| `principal_type` | string | Yes | One of: `user`, `team`, `role` | — |
| `project_id` | string | No | Null for tenant-level permissions | — |
| `component` | string | No | Null for cross-component permissions | — |
| `role_id` | string | Yes | Granted role | — |
| `granted_by` | string | Yes | Actor id of granting administrator | — |
| `granted_at` | timestamp | Yes | Immutable | — |
| `expires_at` | timestamp | No | Null for permanent grants | Required for delegated/time-bounded grants |

#### Authorization model (RBAC + ABAC)

Effective authorization is resolved by `SPMS-PLAT-CORE` (see `SPMS-PLAT-CORE` §13) by combining
role-based grants (above) with attribute-based rules. Permissions resolve in a fixed inheritance
order, most general to most specific, with the most specific applicable rule winning on conflict:

`tenant → project/product → team → object (record) → field/action override`

Attribute-based access control (ABAC) evaluates these attributes when a role grant alone is
insufficient: `classification` of the target vs the principal's `classification_clearance`;
`project_id` / `team_ids` membership; the project or record `governance_profile`; and record
`lifecycle_state` (e.g. baselined records are read-only outside a change request). A field-level
override may further restrict (never broaden) access to individual fields of a record type.

---

## 7.3 Governance entities (SPMS-WF-GOV)

### Workflow

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `workflow_id` | string | Yes | Unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `component` | string | Yes | Owning component code | — |
| `record_type` | string | Yes | Record type this workflow governs | — |
| `version` | integer | Yes | Incremented on each controlled update | — |
| `governance_profile` | string | Yes | One of canonical governance profiles | — |
| `states` | array of objects | Yes | Each: `{name, terminal, side_state}` | Must be a subset of §4 state set |
| `transitions` | array of objects | Yes | Each: `{from_state, to_state, trigger, required_conditions, required_approvals, automatic_actions}` | — |
| `gates` | array of objects | No | Each: `{gate_id, blocking, required_evidence, approvers}` | — |
| `status` | string | Yes | One of: `draft`, `active`, `deprecated` | Only `active` workflows may be applied to records |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |
| `updated_at` | timestamp | Yes | — | — |
| `updated_by` | string | Yes | — | — |

### Approval

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `approval_id` | string | Yes | Unique within tenant | — |
| `tenant_id` | string | Yes | — | — |
| `record_id` | string | Yes | Id of the record requiring approval | — |
| `record_type` | string | Yes | — | — |
| `approval_type` | string | Yes | One of canonical approval types (SPMS-WF-GOV §8.2) | — |
| `requested_by` | string | Yes | Actor id | — |
| `requested_at` | timestamp | Yes | Immutable | — |
| `required_approvers` | array of strings | Yes | User ids or Role ids | — |
| `approval_mode` | string | Yes | One of: `single`, `quorum`, `parallel`, `conditional` | Default `single`; selects the resolution rule below |
| `quorum` | object | No | `{required, of}` — M-of-N threshold | Required when `approval_mode = quorum`; status becomes `approved` once `required` distinct approvers approve |
| `parallel_groups` | array of objects | No | Each: `{group_id, approvers, rule}` where `rule` ∈ `all`,`any` | Required when `approval_mode = parallel`; all groups must satisfy their rule |
| `condition_expr` | string | No | Boolean expression over record attributes (e.g. `classification = restricted OR value > 1e6`) | Required when `approval_mode = conditional`; selects the approver set/route |
| `decisions` | array of objects | No | Each: `{approver_id, decision, decided_at, notes, signature}` | `decision` one of: `approved`, `rejected`, `conditionally_approved` |
| `status` | string | Yes | One of: `pending`, `approved`, `rejected`, `withdrawn`, `expired` | — |
| `expiry` | timestamp | No | Null for non-expiring approvals | — |
| `evidence_refs` | array of strings | No | Evidence record ids linked to this approval decision | — |

The `signature` object inside a decision carries electronic-signature metadata (see `SPMS-WF-GOV`
§9): `{signer_id, signed_at, intent_statement, method (`typed`|`cryptographic`), record_version,
content_hash, non_repudiation_token, certificate_ref}`. The bound `record_version` and
`content_hash` make the signature verifiable against the exact record state that was approved.

---

## 7.4 Evidence entities (SPMS-EVID-AUDIT)

### Evidence

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `evidence_id` | string | Yes | Unique within tenant; immutable | — |
| `tenant_id` | string | Yes | Immutable | — |
| `record_id` | string | Yes | Id of the record this evidence supports | — |
| `evidence_type` | string | Yes | One of: `document`, `test_result`, `scan_report`, `approval_record`, `export`, `screenshot`, `log`, `signature`, `external_reference` | — |
| `title` | string | Yes | 1–500 characters | — |
| `classification` | string | Yes | Inherits from linked record; may be overridden upward | — |
| `object_ref` | string | No | Object storage reference for file-type evidence | Format: `<bucket>/<key>/<hash>` |
| `content_hash` | string | No | SHA-256 of evidence file | Required when `object_ref` is set |
| `retention_class` | string | Yes | One of: `standard`, `long`, `permanent` | Governs object storage WORM policy |
| `uploaded_by` | string | Yes | Actor id; immutable | — |
| `uploaded_at` | timestamp | Yes | Immutable | — |
| `expires_at` | timestamp | No | Null for permanent evidence | Triggers re-validation or stale evidence alert |
| `status` | string | Yes | One of: `valid`, `expired`, `superseded`, `revoked` | — |

### AuditEvent

`AuditEvent` records are append-only. No UPDATE or DELETE is permitted. See SPMS-STD-SEC §7 for tamper-resistance requirements.

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `event_id` | string (UUID v4) | Yes | Immutable; globally unique | Primary key; deduplication key for consumers |
| `tenant_id` | string | Yes | Immutable | — |
| `aggregate_id` | string | Yes | Id of the record or entity that changed | — |
| `aggregate_type` | string | Yes | Record type or entity name | — |
| `event_type` | string | Yes | Registered event type (e.g. `RecordCreated`, `StateChanged`, `ApprovalCompleted`) | — |
| `actor_id` | string | Yes | User id or service id that caused the event | — |
| `actor_type` | string | Yes | One of: `user`, `automation`, `system` | — |
| `payload` | object | Yes | Event-type-specific detail; schema versioned. For mutations, includes a `before`/`after` summary of changed fields | — |
| `schema_version` | string | Yes | Semantic version of the payload schema | e.g. `1.0.0` |
| `occurred_at` | timestamp (ISO 8601, microsecond precision) | Yes | Immutable; time of the originating mutation | — |
| `prev_hash` | string | Yes | SHA-256 of the previous `AuditEvent` in tenant log | Hash chain for tamper resistance (SPMS-STD-SEC §7) |
| `correlation_id` | string | No | Id linking causally related events | — |

### EvidencePackage

An `EvidencePackage` is a reproducible, immutable composition of evidence assembled for an audit,
gate, or release. It must be reconstructable from the stored member records and object references
(see `SPMS-EVID-AUDIT` §9). Corrections are made by superseding the package, never by silent
in-place replacement.

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `package_id` | string | Yes | Unique within tenant; immutable | — |
| `tenant_id` | string | Yes | Immutable | — |
| `project_id` | string | No | Null for tenant-level packages | — |
| `title` | string | Yes | 1–500 characters | — |
| `purpose` | string | Yes | One of: `audit`, `gate`, `release`, `regulatory`, `custom` | — |
| `members` | array of objects | Yes | Each: `{evidence_id, object_ref, content_hash}` | The exact evidence items + content hashes |
| `approval_refs` | array of strings | No | Approval ids included in the package | — |
| `audit_slice_ref` | string | No | Reference to the audit-event range included | Enables historical reconstruction |
| `baseline_refs` | array of strings | No | Baselines the package attests | — |
| `composition_hash` | string | Yes | SHA-256 over the ordered member hashes | Verifies package integrity/reproducibility |
| `status` | string | Yes | One of: `draft`, `sealed`, `superseded` | Only `sealed` packages are citable as audit evidence |
| `sealed_at` | timestamp | No | Set on seal; immutable thereafter | — |
| `sealed_by` | string | No | Actor id; immutable | — |
| `superseded_by` | string | No | Id of superseding package | Never deletes history |

---

## 7.5 Baseline entities (SPMS-BASE-CCB)

### Baseline

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `baseline_id` | string | Yes | Unique within tenant; immutable | — |
| `tenant_id` | string | Yes | Immutable | — |
| `project_id` | string | Yes | — | — |
| `name` | string | Yes | 1–200 characters; unique within project | — |
| `description` | string | No | — | — |
| `baseline_type` | string | Yes | One of: `functional`, `product`, `release`, `audit`, `custom` | — |
| `members` | array of objects | Yes | Each: `{record_id, record_type, version}` — the exact version frozen | Immutable after baseline is sealed |
| `status` | string | Yes | One of: `draft`, `sealed`, `superseded`, `archived` | Only `sealed` baselines may be used for reconstruction |
| `sealed_at` | timestamp | No | Set when status transitions to `sealed`; immutable thereafter | — |
| `sealed_by` | string | No | Actor id; immutable | — |
| `approval_refs` | array of strings | No | Approval ids for the baseline approval | — |
| `evidence_refs` | array of strings | No | Evidence supporting the baseline | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `created_by` | string | Yes | Immutable | — |

### Version

A `Version` is an immutable snapshot of a single `Record` at a specific `version` integer. Versions are created automatically on each controlled update.

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `version_id` | string | Yes | Unique within tenant | — |
| `tenant_id` | string | Yes | Immutable | — |
| `record_id` | string | Yes | Id of the parent record | — |
| `version_number` | integer | Yes | Matches `Record.version` at capture time | — |
| `snapshot` | object | Yes | Full field snapshot of the Record at this version | Immutable |
| `change_summary` | string | No | Human-readable description of what changed | — |
| `changed_by` | string | Yes | Actor id; immutable | — |
| `changed_at` | timestamp | Yes | Immutable | — |

---

## 7.6 Traceability entities (SPMS-TRACE-GRAPH)

### TraceLink

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `link_id` | string | Yes | Unique within tenant; immutable | — |
| `tenant_id` | string | Yes | Immutable | — |
| `project_id` | string | No | Null for cross-project links | — |
| `link_type` | string | Yes | Must be a registered type from §5 | e.g. `SPMS-TRACE-GRAPH-REL-004` |
| `source_id` | string | Yes | Id of the source record | — |
| `source_type` | string | Yes | Record type of the source | — |
| `source_version` | integer | Yes | Version of the source at link creation | Used for suspect-link detection |
| `target_id` | string | Yes | Id of the target record | — |
| `target_type` | string | Yes | Record type of the target | — |
| `target_version` | integer | Yes | Version of the target at link creation | — |
| `suspect` | boolean | Yes | Default false; set true when upstream record changes after link creation | — |
| `suspect_reason` | string | No | Human-readable explanation; required when `suspect=true` | — |
| `rationale` | string | No | Why the link exists; recommended for controlled/critical profiles | Supports explainable traceability |
| `confidence` | number | No | 0.0–1.0; default 1.0 for manually asserted links | Lower for AI-suggested/auto-derived links (`SPMS-AUTO-AI`) |
| `validity_state` | string | Yes | One of: `valid`, `suspect`, `invalid` | `invalid` when an endpoint is retired/deleted or a cardinality/validity rule is violated |
| `evidence_refs` | array of strings | No | Evidence supporting the relationship | — |
| `created_by` | string | Yes | Actor id; immutable | — |
| `created_at` | timestamp | Yes | Immutable | — |
| `status` | string | Yes | One of: `active`, `superseded`, `retracted` | Retracted links are retained for audit |

---

## 7.7 Integration entities (SPMS-INT-EVENT)

### IntegrationEvent

`IntegrationEvent` is the outbox envelope written transactionally alongside each controlled mutation.
See SPMS-STD-EVENT for the full outbox pattern and projection consumption contract.

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `event_id` | string (UUID v4) | Yes | Immutable; globally unique; deduplication key | — |
| `tenant_id` | string | Yes | Immutable | — |
| `aggregate_id` | string | Yes | Id of the mutated record or entity | — |
| `aggregate_type` | string | Yes | Record type or entity name | — |
| `event_type` | string | Yes | Registered event type (matches AuditEvent.event_type) | — |
| `payload` | object | Yes | Event-type-specific; schema versioned | — |
| `schema_version` | string | Yes | Semantic version of payload schema | — |
| `actor_id` | string | Yes | Actor that caused the mutation | — |
| `correlation_id` | string | No | Groups causally related events | — |
| `causation_id` | string | No | `event_id` of the event that caused this one | — |
| `occurred_at` | timestamp (ISO 8601, microsecond precision) | Yes | Immutable; time of originating mutation | — |
| `published_at` | timestamp | No | Null until relay confirms delivery to event bus | Set by outbox relay process |
| `status` | string | Yes | One of: `pending`, `published`, `dead-letter` | Managed by outbox relay |
