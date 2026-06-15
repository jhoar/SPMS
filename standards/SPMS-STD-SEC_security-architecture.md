# Security Architecture Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-SEC |
| Component name | Security Architecture Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Security & Compliance Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | Every component specification |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose and Scope

This standard defines the security architecture for SPMS. All components must comply. Where a
component specification addresses security, it must be consistent with this standard; this
standard governs in any conflict.

This standard covers:
- Tenant isolation model
- ABAC/RBAC evaluation order
- Field-level security
- Service identity model
- Secret-reference handling
- Audit log tamper resistance
- Export-control enforcement
- AI retrieval permission boundaries

# 2. Tenant Isolation Model

## 2.1 Data isolation

`tenant_id` is mandatory on every controlled record (`SPMS-DOMAIN-MODEL` §3) and on every
entity defined in §7 of that document. Isolation is enforced at multiple layers:

| Layer | Mechanism |
|---|---|
| Relational store | Row-level security (RLS) policy on `tenant_id`; no cross-tenant query is permitted at the database layer regardless of application-level checks |
| Graph projection | `tenant_id` included in every graph node and edge; graph queries are always issued with an explicit tenant scope |
| Search index | `tenant_id` included in every index document; queries always filtered by tenant before result ranking |
| Metrics store | `tenant_id` included in every metric series; aggregation never crosses tenant boundary |
| Event bus | `tenant_id` included in every event envelope; consumers must reject events whose `tenant_id` does not match the subscription scope |
| API layer | `tenant_id` derived from the authenticated session token; any mismatch between token tenant and resource tenant is a hard protocol rejection (HTTP 400), not a permission denial (HTTP 403) |
| AI retrieval | Retrieval scope is always bounded to a single tenant; see §9 |

## 2.2 Blast-radius constraint

A defect in one tenant's data path must not expose another tenant's records. This property must
be validated by automated tenant-isolation tests on every pull request. These tests must:
- Create records in Tenant A.
- Authenticate as a valid user of Tenant B.
- Assert that all read, list, search, and export operations return no Tenant A records.
- Assert that write, approve, and link operations on Tenant A records are rejected.

Failure of any tenant-isolation test is a blocking CI gate and must not be merged or deployed.

# 3. ABAC/RBAC Evaluation Order

## 3.1 Evaluation layers

Access control evaluation is strictly layered. The **first DENY terminates the evaluation**; no
subsequent layer can grant access after an earlier denial.

| Layer | Check | Deny condition |
|---|---|---|
| 1. Authentication | Is the actor authenticated and the session token valid and unexpired? | Unauthenticated or expired session |
| 2. Tenant | Does `actor.tenant_id` match `resource.tenant_id`? | Tenant mismatch — protocol error, not permission denial |
| 3. RBAC role | Does the actor's assigned Role grant the requested action on the resource type? | No role grant covers the action |
| 4. ABAC attribute | Do the actor's attribute-based rules permit access to this specific record? | Attribute policy denies access |
| 5. Object-level rule | Does the record's workflow state, lock, or gate permit the operation? | State/lock/gate blocks the operation |
| 6. Field-level | For field-read/write: does the actor's clearance permit access to this specific field? | Field classification exceeds actor clearance |

## 3.2 Supported ABAC attributes

| Attribute | Type | Description |
|---|---|---|
| `actor.tenant_id` | string | Tenant of the authenticated actor |
| `actor.project_ids` | array | Projects the actor is a member of |
| `actor.team_ids` | array | Teams the actor belongs to |
| `actor.role` | string | Actor's assigned role within the relevant scope |
| `actor.classification_clearance` | string | Highest classification level the actor may access |
| `record.owner_id` | string | Owner of the record being accessed |
| `record.classification` | string | Classification of the record |
| `record.project_id` | string | Project the record belongs to |
| `record.lifecycle_state` | string | Current lifecycle state of the record |
| `record.component` | string | Owning component of the record |

# 4. Field-Level Security

## 4.1 Classification-based field access

Records carry a `classification` field (`public`, `internal`, `confidential`, `restricted`).
Actors whose `classification_clearance` is lower than the record's `classification` receive a
redacted view of the record: fields that expose sensitive content are replaced with `[REDACTED]`.
The record itself is visible (it appears in lists and search results) but its sensitive content
is not.

| Record classification | Minimum actor clearance to read full content |
|---|---|
| `public` | Any authenticated actor in the tenant |
| `internal` | `internal` or higher |
| `confidential` | `confidential` or higher |
| `restricted` | `restricted` only |

## 4.2 Write-protected fields

The following fields may only be written by the workflow engine (`SPMS-WF-GOV`) or the platform
itself, never by a direct user API call:

- `lifecycle_state`
- `version`
- `baseline_refs`
- `created_at`, `created_by`
- `superseded_by`

Attempting to set these fields via the record API is a validation error (HTTP 422).

## 4.3 Export field filtering

All export operations (API response, bulk export, report generation) apply field-level
restrictions before serialisation. A restricted field in a record whose classification exceeds
the actor's clearance is omitted from the export, not replaced with a placeholder.

# 5. Service Identity Model

## 5.1 Service tokens

Services communicate using scoped service tokens issued by the platform identity service, not
user session tokens. A service token carries:

| Claim | Description |
|---|---|
| `service_id` | Stable identity of the service or automation actor |
| `tenant_id` | Tenant scope (`*` only for platform-level administrative services) |
| `allowed_scopes` | Array of permitted action scopes (e.g., `record:read`, `event:publish`) |
| `issued_at` | Token issuance timestamp |
| `expires_at` | Token expiry; services must refresh before expiry |

## 5.2 Automation actors

Automation actors (rules engine, scheduled jobs, AI assistance functions, outbox relay) act
under their service identity. All mutations they perform must:
- Include `actor_id` = service identity in the produced `AuditEvent`.
- Set `actor_type = automation` in the `AuditEvent`.
- Respect the same ABAC/RBAC evaluation order (§3) as human actors.

## 5.3 User impersonation prohibition

No service may act on behalf of a user (impersonate) unless the user has explicitly delegated
authority via the `SPMS-WF-GOV` delegation workflow. Delegated actions must carry both the
service identity and the delegating user's id in the `AuditEvent`.

# 6. Secret-Reference Handling

## 6.1 Prohibition on raw secrets

Raw secret values must never be stored in:
- Controlled record fields or `metadata`
- `IntegrationEvent` or `AuditEvent` payloads
- Configuration objects in the relational store
- Log output, traces, or error messages

## 6.2 Secret reference format

All references to secrets use the canonical format:

```
secret:<provider>:<name>:<version>
```

Examples:
- `secret:vault:db-password:3`
- `secret:aws-sm:api-key-prod:7`

The platform resolves references at runtime by calling the configured external secret manager.
Resolution must never cache the resolved value in a location that is logged or persisted.

## 6.3 Resolution audit

Each secret resolution event (by name and version, not value) must produce an `AuditEvent` of
type `SecretResolved` including `actor_id`, `secret_name`, `secret_version`, and `occurred_at`.
Secret values are never included.

## 6.4 Rotation handling

When a secret version changes in the external manager, the platform must:
- Flag any integration configuration that references the previous version.
- Notify the integration owner.
- Prevent new connections from using the stale reference after the rotation grace period.

# 7. Audit Log Tamper Resistance

## 7.1 Append-only constraint

`AuditEvent` records are append-only. No UPDATE or DELETE operation is permitted on the audit
log table at any layer (application, migration, administrative tooling). Any schema migration
that would affect existing `AuditEvent` rows must be rejected at review.

## 7.2 Hash chain

Each `AuditEvent` includes a `prev_hash` field containing the SHA-256 hash of the previous
`AuditEvent` in the tenant's log (ordered by `occurred_at`). This forms a tamper-evident hash
chain. The first event in a tenant's log has `prev_hash = NULL`.

Hash chain validation must be:
- Available on-demand via an auditor API endpoint (returns: valid / invalid + first-failing event).
- Run on a scheduled basis (minimum daily) as an automated integrity check.
- Triggered automatically before producing any compliance or audit export package.

## 7.3 WORM storage for evidence

Object storage used for evidence files (`SPMS-EVID-AUDIT`) must be configured as WORM (Write
Once Read Many) for the retention period defined by the evidence record's `retention_class`.
WORM configuration must prevent deletion or overwrite by any actor, including platform
administrators, for the retention duration.

# 8. Export-Control Enforcement

## 8.1 Pre-export classification check

Before serialising any record for export (API response, bulk export, report, evidence package),
the platform evaluates Layer 6 (field-level) of the access control evaluation order (§3.1) for
every field in every record included in the export.

## 8.2 Approval for sensitive exports

| Export type | Minimum approval required |
|---|---|
| Single record API response | ABAC/RBAC check only (§3) |
| Bulk export of `public` or `internal` records | ABAC/RBAC check only |
| Bulk export of `confidential` records | Explicit `export` permission required |
| Bulk export of `restricted` records | `export` permission + approval via `SPMS-WF-GOV` |
| Compliance audit package | PA/QA approval (`SPMS-WF-GOV` §8.2) |

## 8.3 Export audit

Every export operation must produce an `AuditEvent` of type `RecordExported` containing:
- `actor_id`
- Array of exported record ids (or count + filter criteria for large exports)
- `classification` of the highest-classified record in the export
- Export format (JSON, CSV, PDF, etc.)
- `occurred_at`

# 9. AI Retrieval Permission Boundaries

## 9.1 Permission check before retrieval

The AI retrieval layer (`SPMS-AUTO-AI`) must evaluate the full ABAC/RBAC stack (§3.1, layers
1–6) for every candidate record before including it in the retrieval context sent to the AI
model. Records that fail any access check are excluded from retrieval silently — they must not
appear in the context, the response, or the Grounding Attestation.

## 9.2 Tenant scope

The AI function's service identity (§5) is always scoped to a single tenant. Cross-tenant
retrieval is prohibited even if the requesting user has a valid session in multiple tenants.
Each AI request is issued within one tenant context and returns only that tenant's records.

## 9.3 Classification boundary

Records with `classification: restricted` are excluded from AI retrieval unless the requesting
actor has `classification_clearance: restricted`. This check is applied at retrieval time, not
at model-response generation time, to prevent inadvertent leakage through retrieved context.

## 9.4 Grounding Attestation classification disclosure

The Grounding Attestation required by `SPMS-AUTO-AI` §22.2 must include the `classification`
of each retrieved record. This allows auditors to verify that the AI function operated within
the actor's permission boundary.
