# Configuration Governance Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-CONFIG |
| Component name | Configuration Governance Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board; Security & Compliance Lead |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | All SPMS components; all tenant and project administrators |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

This standard bounds the configurability of the SPMS platform so that tenants cannot diverge
in ways that break cross-tenant reporting, audit consistency, or the canonical domain model.
It classifies every configurable surface into one of three tiers (§2), defines the scope
hierarchy and precedence rules for configuration (§3), mandates controlled-change governance for
non-trivial configuration changes (§4), and establishes the consistency guardrails that protect
cross-tenant data comparability (§5).

This standard is the structural mitigation for the per-specification `R-001` over-customization
risk and is promoted to a programme-level risk as `RISK-011` in `SPMS-DELIVERY`.

# 2. Configuration Taxonomy

All configurable surfaces in the SPMS platform are classified into exactly one of the following
tiers. The tier determines what a tenant or project administrator may change, and what the
platform unconditionally enforces.

## 2.1 Fixed (Canonical, Non-Configurable)

The following elements are part of the canonical SPMS platform and may not be altered, removed,
or redefined by any tenant, project, or platform operator:

| Element | Canonical source | Rationale |
|---|---|---|
| Common Record Model fields (`id`, `tenant_id`, `project_id`, `record_type`, `lifecycle_state`, `version`, `created_at`, `updated_at`, `created_by`, `classification`) | `SPMS-DOMAIN-MODEL §3` | Cross-tenant reporting and audit depend on universal field presence |
| Canonical lifecycle state set (`draft`, `in_review`, `approved`, `baselined`, `in_change`, `verified`, `accepted`, `retired`, `archived`, `withdrawn`) | `SPMS-DOMAIN-MODEL §4` | Workflow gates, reporting dashboards, and compliance mappings reference the canonical set by name |
| Registered link types (the controlled link-type registry) | `SPMS-DOMAIN-MODEL §5` | Traceability matrices, impact analysis, and coverage reports use the canonical link vocabulary |
| `AuditEvent` schema (`event_id`, `tenant_id`, `actor_id`, `event_type`, `target_id`, `target_type`, `timestamp`, `prev_hash`, `payload`) | `SPMS-DOMAIN-MODEL §7.4` | Audit chain integrity (`SPMS-STD-INVARIANTS INV-001`) depends on a fixed schema |
| Identifier scheme (namespace, three-digit capability padding, separator conventions) | `SPMS-STD-ID` | Cross-component references and linter checks depend on a stable scheme |
| Security classification tiers and export-control rules | `SPMS-STD-SEC §8` | Export filtering and audit obligations are defined against fixed tier names |

A platform component that allows a tenant to redefine any Fixed element must be treated as a
critical defect and blocked from release.

## 2.2 Canonical-Constrained (Configurable Within Rails)

The following surfaces may be configured by tenant or project administrators, but only within
the constraints stated. The platform must enforce these rails at write time and reject any
configuration that violates them.

| Surface | What may be configured | What is enforced |
|---|---|---|
| Workflows | Custom state names, transitions, and gate conditions | Every custom state must map to one canonical lifecycle state; no transition may skip a mandatory gate (`SPMS-WF-GOV §5`) |
| Metadata schema | Addition of new typed fields to any record type; field-level labels, descriptions, and display order | Addition only — canonical fields may not be renamed, removed, or have their type changed; new fields must have a declared type (`string`, `integer`, `date`, `enum`, `reference`) |
| Governance profile selection | Select one of the five defined profiles for a project | Profile set is fixed (Lightweight / Low-risk bulk / Standard / Controlled / Critical); custom profiles are not permitted |
| Retention periods | Extend retention beyond regulatory minimums | May not be set below the regulatory minimum for the record type and jurisdiction; default minimums are defined by the platform operator |
| Approval gates | Add extra approval stages to a workflow | Mandatory gates defined by `SPMS-WF-GOV` may not be removed or made optional; additional gates may be added |
| Notification rules | Subscribe users/roles to events; configure delivery channels | Cannot suppress mandatory audit notifications; cannot route notifications outside tenant-controlled endpoints |
| Import field mappings | Map source-system fields to SPMS fields | Target fields must exist in the SPMS schema; canonical Common Record Model fields may not be overridden by a mapping |

Configuration changes to Canonical-Constrained surfaces must pass validation before activation.
The platform must reject invalid configurations with a structured error identifying the violated
constraint.

## 2.3 Free (Tenant-Local)

The following surfaces may be configured without restriction and do not affect cross-tenant
data consistency:

- Branding: logos, colour themes, custom domain names.
- Notification preferences: per-user opt-in/opt-out for non-mandatory notifications.
- Saved views and filters: personal or team-scoped search presets.
- Dashboard layouts: widget arrangement, default dashboard per role.
- Non-controlled labels and tags: non-structural metadata applied to records for filtering.
- Email and calendar integration preferences.
- Report export template formatting (not content or field selection).

Free-tier changes do not require change-control approval but are still recorded as `AuditEvent`
entries (event type `ConfigurationChanged`, level `Free`) so that configuration history is
reconstructable.

# 3. Configuration Scopes

SPMS configuration is organised into three nested scopes. Configuration at a narrower scope
overrides the same setting at a broader scope, subject to the Fixed and Canonical-Constrained
rails in §2.

| Scope | Managed by | Override rules |
|---|---|---|
| **Platform** | Platform operator | Sets defaults and hard limits. Fixed elements in §2.1 are enforced here unconditionally. |
| **Tenant** | Tenant administrator | May override platform defaults within Canonical-Constrained rails. May not touch Fixed elements. |
| **Project** | Project administrator | May override tenant defaults within Canonical-Constrained rails. May not loosen tenant-set constraints. |

**Precedence:** Platform-Fixed always wins. Within the Canonical-Constrained tier, the
narrowest scope that specifies a value wins (Project > Tenant > Platform default), provided the
narrower value does not violate the constraint set by the immediately broader scope.

This hierarchy is defined by the `Tenant` and `Project` entity schemas in
`SPMS-DOMAIN-MODEL §7.2`. The admin configuration UX (`SPMS-UX §9`) presents each scope's
settings in separate, clearly labelled sections so administrators cannot accidentally conflate
scope levels.

# 4. Configuration Change Governance

Configuration changes are controlled changes. The level of control required depends on the
impacted tier.

| Configuration tier | Change control level | Approval requirement |
|---|---|---|
| Fixed (§2.1) | Not applicable — changes are platform defects, not configuration | Engineering Director sign-off to release a corrective build |
| Canonical-Constrained — workflow / schema / identity / retention changes | Level 2/3 (`SPMS-METHODOLOGY`) | Tenant administrator + project lead; audited |
| Canonical-Constrained — gate additions / notification rule changes | Level 2 (`SPMS-METHODOLOGY`) | Tenant administrator; audited |
| Free (§2.3) | Level 1 (`SPMS-METHODOLOGY`) | Self-service; audited |

**Every configuration change must:**
1. Emit an `AuditEvent` record of type `ConfigurationChanged` with a `payload` that captures
   the changed surface, the previous value, and the new value (`SPMS-STD-MODULE §6`).
2. Support a dry-run / preview mode where the change would affect existing records (e.g.
   metadata field removal, retention reduction, workflow state rename), per `SPMS-UX §9.4`.
3. Be reversible by the same administrator or by a platform operator within the retention window,
   except where the reversal would break audit chain continuity or baseline immutability.

Configuration changes to Canonical-Constrained surfaces that affect existing records must
be previewed before activation. The preview must display the number of affected records and any
records that would enter an invalid state.

# 5. Consistency Guardrails

The following rules protect cross-tenant reporting, audit integrity, and the canonical domain
model. Each guardrail names the invariant it preserves.

**G-001 Lifecycle state mapping.** Every tenant-defined custom state in a workflow must carry a
`canonical_state` attribute that maps it to one of the canonical lifecycle states (§2.1). The
platform must refuse to activate a workflow that contains an unmapped state. Cross-module
reporting and compliance dashboards use only the canonical state set; custom states are displayed
locally but aggregated to their canonical equivalents in cross-tenant views. This guardrail
preserves `SPMS-STD-INVARIANTS INV-002` (historical reconstruction fidelity).

**G-002 Link type restriction.** `TraceLink` records may only be created with link types drawn
from the registered link-type vocabulary (`SPMS-DOMAIN-MODEL §5`). Tenant administrators may
not define new link types unilaterally; new link types require platform-level registration via
the link-type governance process. This guardrail preserves `SPMS-STD-INVARIANTS INV-003`
(graph↔relational consistency).

**G-003 Metadata additivity.** Tenant and project metadata schema extensions are additive only.
Canonical Common Record Model fields (§2.1) may not be removed, renamed, or have their data
type changed. New fields introduced at the tenant or project scope are prefixed with the tenant
or project identifier to avoid collision with future canonical fields. This guardrail preserves
search and report field coherence across tenants.

**G-004 Classification taxonomy.** The security classification tiers and their export-control
implications are Fixed (§2.1) and may not be altered. Tenants may not add classification tiers
above or between the canonical set. This guardrail preserves `SPMS-STD-SEC §8` export rules and
ensures that inter-tenant audit package exchanges have consistent classification semantics.

**G-005 Audit schema immutability.** The `AuditEvent` schema (§2.1) may not be extended by
tenants or projects. All supplementary context must be placed in the structured `payload` field
as typed JSON. This guardrail preserves `SPMS-STD-INVARIANTS INV-001` (audit append-only +
hash chain).

**G-006 Retention minimums.** Retention periods for controlled record types and audit events
may not be set below the platform-defined regulatory minimums for the record type and
jurisdiction. Platform minimums are derived from applicable regulatory frameworks and reviewed
at least annually by the Programme Technical Authority. This guardrail preserves audit
completeness and legal defensibility.

Each guardrail is enforced at write time by the platform. A configuration change that violates
a guardrail is rejected with a structured error identifying the guardrail ID, the violated
constraint, and the value that was rejected.

# 6. Configuration Baselining and Drift Detection

Tenant and project configuration is itself a versioned artefact that participates in the
baseline and change-control lifecycle.

**Configuration versioning.** Every change to a Canonical-Constrained configuration surface
increments a `config_version` counter for the affected tenant or project scope. The platform
retains the full configuration history for the retention period, enabling reconstruction of the
configuration state at any past point in time (consistent with `SPMS-STD-INVARIANTS INV-002`).

**Configuration baselining.** A tenant or project administrator may create a `ConfigurationBaseline`
(a specialisation of `Baseline` in `SPMS-BASE-CCB`) that captures a named, immutable snapshot
of the tenant or project configuration. Configuration baselines are governed by the same
immutability rules as record baselines (`SPMS-STD-INVARIANTS INV-004`).

**Drift detection.** The platform computes and reports configuration drift: the set of
Canonical-Constrained settings that have changed since the most recently approved
`ConfigurationBaseline`. Drift is surfaced in the tenant administration console and in
compliance reports. Drift from an approved configuration baseline is flagged as a finding in
the product assurance dashboard (`SPMS-PROD-ASSUR`), mirroring the asset drift detection in
`SPMS-CFG-ASSET`.

# 7. Cross-References

| Document | Relationship |
|---|---|
| `SPMS-DOMAIN-MODEL` | Common Record Model fields (§3), lifecycle state set (§4), link-type registry (§5), entity schemas (§7) |
| `SPMS-WF-GOV` | Workflow configuration, governance profile definitions, mandatory gate catalogue |
| `SPMS-METHODOLOGY` | Change control levels (Level 1/2/3) used in §4 |
| `SPMS-STD-MODULE` | Shared audit event requirements (§6); all modules must honour `ConfigurationChanged` events |
| `SPMS-STD-INVARIANTS` | INV-001 (audit schema), INV-002 (workflow state mapping), INV-003 (link type restriction), INV-004 (configuration baseline immutability) |
| `SPMS-STD-SEC` | Classification tiers and export-control rules (§8); field-level security (§4) |
| `SPMS-UX §9` | Admin configuration UX, dry-run/preview flows (§9.4), scope-level settings separation |
| `SPMS-BASE-CCB` | Baseline lifecycle; `ConfigurationBaseline` specialisation |
| `SPMS-CFG-ASSET` | Asset drift detection pattern applied to configuration drift (§6) |
| `SPMS-DELIVERY` | RISK-011 (over-configuration / tenant divergence) |

# 8. Governance, Approvals, Waivers, and Gates

A waiver permitting a tenant to operate outside the Canonical-Constrained rails requires:
1. Written justification from the tenant administrator identifying the surface, the constraint
   being relaxed, and the technical necessity.
2. Impact assessment showing no effect on cross-tenant reporting, audit integrity, or link
   consistency.
3. Sign-off by the Programme Technical Authority and the Security & Compliance Lead.
4. A time-bounded remediation plan with a deadline no later than the next major release.

Waivers are recorded as `AuditEvent` records of type `WaiverGranted` and appear in the tenant's
configuration drift report.

No waiver may permit overriding Fixed elements (§2.1). Any request to modify Fixed elements
must be treated as a platform change request, not a configuration waiver.

# 9. Evidence, Audit, and Historical Reconstruction

All configuration changes (Fixed, Canonical-Constrained, and Free) are recorded as `AuditEvent`
entries as specified in §4. The audit trail for configuration must support the same historical
reconstruction guarantee as controlled records: given a tenant ID and a point in time, the
active configuration at that time must be reconstructable from the event log.

Configuration baseline snapshots are subject to `SPMS-STD-INVARIANTS INV-004` (baseline
immutability): once sealed, a `ConfigurationBaseline` may not be modified and its content must
remain retrievable verbatim for the retention period.
