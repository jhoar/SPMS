# Platform Core Specification

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-PLAT-CORE |
| Component name | Platform Core |
| Component type | Platform substrate |
| Version | 0.2 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Platform Architecture Lead |
| Authors | System architecture team |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-05-17 |
| Last updated | 2026-06-16 |
| Authoritative | Yes |
| Supersedes | SPMS-SUB-001; SPMS-SUB-002 (record-model portion); SPMS-SUB-010 (admin/ops portion) |
| Specification register | SPMS-INDEX |
| Canonical domain model | SPMS-DOMAIN-MODEL |
| Identifier standard | SPMS-STD-ID |
| Target release / baseline | Foundation baseline / Module baseline |
| Related specifications | Platform Core, Workflow & Governance Core, Traceability Graph Core, Evidence & Audit Core, Planning & Work Packages, Issue & Change Management, Requirements Management, Document & Knowledge Management, Test/V&V Management, Build & CI/CD Management, Release & Deployment Management, Configuration & Asset Management, Security & Compliance Management, Product Assurance, Reporting & Analytics, Automation & AI Assistance |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set. It supersedes the
> superseded draft(s) listed in Document Control. For the controlling register, identifier rules,
> canonical domain model, scale envelope, and delivery methodology, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.
> Where this document and any superseded draft differ, this document governs. Net-new detail in
> superseded drafts is tracked in `DETAIL-HARVEST-BACKLOG` for incorporation during detailed design.

# 1. Purpose and Scope

## 1.1 Purpose

Provides the shared organisational, identity, permission, and metadata foundation for every module.

## 1.2 Scope

This component includes:

- Tenant and workspace management.
- Project/product/team registry.
- Identity and access management.
- Metadata and taxonomy management.
- Common object model.
- Notification and activity substrate.
- Administration console.
- Platform operations and resilience.

This component excludes:

- Final business ownership decisions, which are configured per tenant/project.
- Raw secret value storage; only approved secret references are permitted.
- Uncontrolled modification of approved, baselined, accepted, or audited records.

## 1.3 Component Classification

| Field | Value |
|---|---|
| Module category | Foundation |
| Mandatory for minimal deployment? | Yes |
| Mandatory for governed deployment? | Yes |
| Supports single-project mode? | Yes |
| Supports multi-project mode? | Yes |
| Supports multi-tenant mode? | Yes |
| Can be disabled? | No |

---

# 2. Context in the Overall Architecture

## 2.1 Architectural Role

Platform Core is a shared foundation service in the modular Software Project Management System. It uses Platform Core for identity, tenants, permissions, metadata, and administration; Workflow & Governance Core for lifecycle, approvals, gates, delegation, SoD, and SLAs; Traceability Graph Core for links and impact analysis; and Evidence & Audit Core for evidence, immutable history, and audit packages.

## 2.2 Upstream and Downstream Dependencies

| Dependency | Direction | Type | Description |
|---|---|---|---|
| Platform Core | Upstream | Data / Security / UI | Tenant, project, product, team, identity, permissions, metadata, classifications. |
| Workflow & Governance Core | Bidirectional | Workflow / Event | State transitions, approvals, gates, delegation, SoD, SLA timers. |
| Traceability Graph Core | Bidirectional | Data / API | Links, impact analysis, matrices, coverage, topology, suspect links. |
| Evidence & Audit Core | Bidirectional | Data / Event | Evidence records, object references, immutable audit events, packages. |
| Reporting & Analytics | Downstream | Data / Event | Metrics, dashboards, trends, exports, executive views. |
| Automation & AI Assistance | Bidirectional | Event / API | Rules, policy-as-code, scheduled jobs, suggestions, grounded Q&A. |

## 2.3 Related Components

| Component | Relationship |
|---|---|
| Platform Core | This specification. |
| Workflow & Governance Core | Depends on or is served by this shared component. |
| Traceability Graph Core | Depends on or is served by this shared component. |
| Evidence & Audit Core | Depends on or is served by this shared component. |
| Planning & Work Packages | Depends on or is served by this shared component. |
| Issue & Change Management | Depends on or is served by this shared component. |
| Requirements Management | Depends on or is served by this shared component. |
| Document & Knowledge Management | Depends on or is served by this shared component. |
| Test/V&V Management | Depends on or is served by this shared component. |
| Build & CI/CD Management | Depends on or is served by this shared component. |
| Release & Deployment Management | Depends on or is served by this shared component. |
| Configuration & Asset Management | Depends on or is served by this shared component. |
| Security & Compliance Management | Depends on or is served by this shared component. |
| Product Assurance | Depends on or is served by this shared component. |
| Reporting & Analytics | Depends on or is served by this shared component. |
| Automation & AI Assistance | Depends on or is served by this shared component. |

---

# 3. Users, Roles, and Responsibilities

## 3.1 User Types

| User type | Description | Typical permissions |
|---|---|---|
| Administrator | Configures the component and its policies. | Configure, administer, monitor, migrate. |
| Owner | Accountable for records or configuration in this component. | Create, review, approve where authorised, close. |
| Contributor | Creates or modifies records. | Create, edit drafts, comment, attach evidence. |
| Reviewer | Reviews records, evidence, or changes. | Review, comment, request changes, recommend approval. |
| Approver | Provides formal approval. | Approve, reject, conditionally approve, request rework. |
| Viewer | Reads information. | Read permitted records, dashboards, reports. |
| Auditor | Reviews historical state and evidence. | Read audit trails, exports, baselines, evidence packages. |
| External collaborator | Customer, supplier, partner, regulator, or auditor. | Restricted review/comment/approval/export as configured. |
| Automation actor | System, integration, agent, bot, or scheduled job. | API actions under scoped service identity. |

## 3.2 Role Model

| Role | Responsibilities | Authority | Separation-of-duty constraints |
|---|---|---|---|
| Component administrator | Configure schemas, workflows, integrations, retention, and views. | Administrative authority within assigned tenant/project. | Cannot self-approve controlled records unless explicitly allowed in lightweight profile. |
| Record owner | Maintain correctness, completeness, and timely closure. | Owns records and may submit for review. | Cannot independently approve own controlled changes in controlled/critical profiles. |
| Technical reviewer | Assess technical correctness and completeness. | Recommend approval or request changes. | Must be independent where configured. |
| Governance approver | Make formal gate, baseline, waiver, or acceptance decisions. | Approve/reject controlled records and gates. | Cannot be requester for same approval in controlled/critical profiles. |
| Auditor | Inspect evidence, history, and compliance. | Read-only access to audit scope. | Cannot modify audited records. |
| Automation service | Execute rules and integrations. | Scoped API permissions only. | Cannot perform human approvals. |

## 3.3 RACI Matrix

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Create record | Contributor / Automation actor | Owner | Reviewer | Watchers / Team |
| Review record | Reviewer | Owner | Contributor | Approver |
| Approve record | Approver | Governance authority | Reviewer / Owner | Stakeholders |
| Change approved record | Owner / Contributor | Approver | Traceability and assurance roles | Affected users |
| Close / retire record | Owner | Approver where controlled | Reviewer / Auditor | Stakeholders |
| Export audit package | Auditor / Administrator | Governance authority | Owner | Audit recipients |

---

# 4. Functional Capabilities

## 4.1 Capability Summary

| Capability ID | Capability name | Description | Priority | Required for minimal mode? |
|---|---|---|---|---|
| SPMS-PLAT-CORE-CAP-001 | Tenant and workspace management | Provides tenant and workspace management for Platform Core. | Must | Yes |
| SPMS-PLAT-CORE-CAP-002 | Project/product/team registry | Provides project/product/team registry for Platform Core. | Must | Yes |
| SPMS-PLAT-CORE-CAP-003 | Identity and access management | Provides identity and access management for Platform Core. | Must | Yes |
| SPMS-PLAT-CORE-CAP-004 | Metadata and taxonomy management | Provides metadata and taxonomy management for Platform Core. | Must | Yes |
| SPMS-PLAT-CORE-CAP-005 | Common object model | Provides common object model for Platform Core. | Should | Yes |
| SPMS-PLAT-CORE-CAP-006 | Notification and activity substrate | Provides notification and activity substrate for Platform Core. | Should | Yes |
| SPMS-PLAT-CORE-CAP-007 | Administration console | Provides administration console for Platform Core. | Should | Yes |
| SPMS-PLAT-CORE-CAP-008 | Platform operations and resilience | Provides platform operations and resilience for Platform Core. | Should | Yes |
| SPMS-PLAT-CORE-CAP-009 | RBAC and ABAC authorization | Resolves effective authorization from role grants and attribute-based rules. | Must | Yes |
| SPMS-PLAT-CORE-CAP-010 | Object and field-level permissions | Enforces per-object and per-field permission overrides. | Must | Yes |
| SPMS-PLAT-CORE-CAP-011 | Approval authority and delegation | Manages who may approve and time-bounded delegation of authority. | Must | Yes |
| SPMS-PLAT-CORE-CAP-012 | Separation of duties | Enforces incompatible-role and requester/approver constraints. | Should | Yes |
| SPMS-PLAT-CORE-CAP-013 | Access review and evidence | Runs periodic access reviews and produces access evidence. | Should | No |
| SPMS-PLAT-CORE-CAP-014 | Custom fields and validation | Defines custom fields and validation rules per record type. | Should | Yes |
| SPMS-PLAT-CORE-CAP-015 | Record quality checks | Validates record completeness and quality against policy. | Should | No |
| SPMS-PLAT-CORE-CAP-016 | Retention and legal-hold administration | Administers retention policies and legal holds across record types. | Should | Yes |
| SPMS-PLAT-CORE-CAP-017 | Feature flag management | Manages platform/tenant feature flags. | Should | No |
| SPMS-PLAT-CORE-CAP-018 | Observability and alerting | Provides health signals, metrics, and alerting for the platform. | Should | Yes |

## 4.2 Capability Details

## Capability: `Tenant and workspace management`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-001 |
| Purpose | Support tenant and workspace management within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Project/product/team registry`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-002 |
| Purpose | Support project/product/team registry within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Identity and access management`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-003 |
| Purpose | Support identity and access management within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Metadata and taxonomy management`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-004 |
| Purpose | Support metadata and taxonomy management within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Common object model`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-005 |
| Purpose | Support common object model within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Notification and activity substrate`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-006 |
| Purpose | Support notification and activity substrate within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Administration console`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-007 |
| Purpose | Support administration console within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `Platform operations and resilience`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-008 |
| Purpose | Support platform operations and resilience within the Platform Core component. |
| Trigger | Manual / Scheduled / Event-driven / API / Integration / AI-assisted |
| Primary users | Administrator; Owner; Contributor; Reviewer; Approver; Auditor; Automation actor |
| Inputs | Platform Core records, related links, metadata, policy configuration, comments, evidence, and events. |
| Outputs | Updated Platform Core records, state changes, evidence links, audit events, notifications, metrics, and reports. |
| Preconditions | Actor is authenticated; permissions and workflow state allow the operation; required upstream records exist where applicable. |
| Postconditions | Record state, links, evidence, events, metrics, and audit history are consistent and queryable. |
| Main workflow | Create or select record; validate required fields; apply workflow/policy rules; update relationships; collect evidence; notify affected users; emit audit/event records. |
| Alternate workflows | Bulk import; API update; automation-triggered update; delegated approval; waiver/deviation route; read-only external collaboration. |
| Error / exception handling | Reject invalid transitions; record validation errors; support rollback where safe; create issue/NCR for controlled failures; preserve failed automation evidence. |
| Related records | Tenant, Project, Product, Team, User; approvals; baselines; evidence; trace links; reports. |
| Required evidence | Defined by governance profile; may include approval records, review notes, generated reports, logs, exports, or external tool evidence. |
| Required approvals | Owner approval for controlled changes; specialist approval where configured; baseline/release/acceptance approval when the record gates downstream decisions. |
| Audit requirements | Audit creation, edits, workflow transitions, approvals, evidence changes, import/export, link changes, and permission-sensitive access. |
| Metrics produced | Volume, throughput, cycle time, aging, backlog, readiness, evidence completeness, approval latency, exception count, and trend indicators. |
| Configuration options | Field schema, workflow, roles, approval policy, retention, notifications, views, import mappings, and automation rules. |

## Capability: `RBAC and ABAC authorization`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-009 |
| Purpose | Resolve effective authorization for every request by combining role-based grants with attribute-based rules, applying a fixed permission-inheritance order. |
| Trigger | API / Event-driven (every authorization decision) |
| Primary users | All users (subject); Administrator (policy author); Auditor |
| Inputs | Principal (user/team/role/service account), target record + attributes, role grants, and ABAC rules. |
| Outputs | Allow/deny decisions, decision rationale, and audit events for sensitive decisions. |
| Preconditions | Principal is authenticated; target and its classification/scope are resolvable. |
| Postconditions | The decision is consistent with the inheritance order and ABAC attributes and is explainable. |
| Main workflow | Resolve grants in order tenant → project/product → team → object → field/action override; evaluate ABAC attributes (classification clearance, membership, governance profile, lifecycle state); return the most-specific decision. |
| Alternate workflows | Service-account authorization; delegated authority; external-collaborator restricted access. |
| Error / exception handling | Deny by default on ambiguity; record denied sensitive access; preserve decision inputs for audit. |
| Related records | User, Role, Permission, Group, ServiceAccount; records being accessed. |
| Required evidence | Decision audit for access-sensitive operations. |
| Required approvals | None for decisions; policy changes follow admin approval. |
| Audit requirements | Audit permission changes and access-sensitive denials/grants. |
| Metrics produced | Authorization latency, deny rate, and policy-conflict count. |
| Configuration options | Role definitions, ABAC attribute set, and default-deny policy. |

## Capability: `Object and field-level permissions`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-010 |
| Purpose | Enforce per-object and per-field permission overrides that may further restrict (never broaden) access granted at higher scopes. |
| Trigger | API / Event-driven |
| Primary users | Administrator; Owner; Auditor |
| Inputs | Object/field override rules, record type field definitions, and the resolved higher-scope decision. |
| Outputs | Field-filtered records and per-field allow/deny decisions. |
| Preconditions | A higher-scope decision exists; field definitions are registered. |
| Postconditions | Restricted fields are hidden/blocked even when the record is otherwise readable. |
| Main workflow | Apply object-level override; apply field-level override; return the intersection (most restrictive) result. |
| Alternate workflows | Bulk field-policy application; API field projection; export with field redaction. |
| Error / exception handling | Default to most restrictive on conflict; never allow an override to broaden access; audit field-policy changes. |
| Related records | FieldDefinition, RecordType, Permission; records being accessed. |
| Required evidence | Audit of field-policy changes. |
| Required approvals | Administrator approval for field-policy changes. |
| Audit requirements | Audit object/field override changes. |
| Metrics produced | Field-restriction coverage and override-conflict count. |
| Configuration options | Object/field override rules and redaction behaviour. |

## Capability: `Approval authority and delegation`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-011 |
| Purpose | Manage which identities hold approval authority and support time-bounded, scoped delegation of that authority (the identity side; the approval workflow itself is owned by `SPMS-WF-GOV`). |
| Trigger | Manual / API / Event-driven |
| Primary users | Administrator; Owner; Approver; Auditor |
| Inputs | Authority assignments, delegation requests, scope, and expiry. |
| Outputs | `Delegation` records, effective-authority resolution, and audit events. |
| Preconditions | The delegating principal holds the authority; the delegate is an eligible identity. |
| Postconditions | Delegated authority is time-bounded, scoped, visible in approval records, and never erases the original authority. |
| Main workflow | Create delegation with scope and expiry; resolve effective authority at approval time; expire/revoke; emit audit/event records. |
| Alternate workflows | Emergency delegation; automation-flagged expiring delegation. |
| Error / exception handling | Reject delegation exceeding the delegator's authority or violating SoD; preserve delegation evidence. |
| Related records | Delegation, User, Role; approval records (`SPMS-WF-GOV`). |
| Required evidence | Delegation records and their scope/expiry. |
| Required approvals | Administrator approval for standing delegations where configured. |
| Audit requirements | Audit delegation creation, use, and revocation. |
| Metrics produced | Active-delegation count and expired-but-used attempts. |
| Configuration options | Delegation policy, default expiry, and SoD compatibility rules. |

## Capability: `Separation of duties`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-012 |
| Purpose | Enforce incompatible-role and requester/approver constraints on the identity side so conflicting authorities are not combined. |
| Trigger | API / Event-driven |
| Primary users | Administrator; Approver; Auditor |
| Inputs | SoD rule set, principal's roles/grants, and the action being attempted. |
| Outputs | SoD allow/deny decisions and conflict findings. |
| Preconditions | SoD rules are configured; principal roles are resolvable. |
| Postconditions | Conflicting authorities are blocked or flagged per policy. |
| Main workflow | Evaluate the attempted action against SoD rules; block requester==approver and incompatible-role combinations; record conflicts. |
| Alternate workflows | Toxic-combination report; periodic SoD review; waiver-backed exception (`SPMS-WF-GOV`). |
| Error / exception handling | Default to deny on conflict; require waiver for exceptions; audit conflicts. |
| Related records | Role, Permission, User; AccessReview. |
| Required evidence | SoD conflict findings and any waivers. |
| Required approvals | Governance approval for SoD exceptions. |
| Audit requirements | Audit SoD denials and exceptions. |
| Metrics produced | SoD conflict count and exception rate. |
| Configuration options | SoD rule set and exception policy. |

## Capability: `Access review and evidence`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-013 |
| Purpose | Run periodic access reviews (recertification) and produce access evidence for audit. |
| Trigger | Scheduled / On demand |
| Primary users | Administrator; Owner; Reviewer; Auditor |
| Inputs | Current grants, review scope/schedule, and reviewers. |
| Outputs | `AccessReview` records, recertification decisions, revocations, and evidence. |
| Preconditions | Grants exist; reviewers are assigned. |
| Postconditions | Access is recertified or revoked, with evidence retained. |
| Main workflow | Generate review campaign; reviewers certify/revoke each grant; apply revocations; emit audit/event records. |
| Alternate workflows | Ad-hoc review; automation-driven anomaly review. |
| Error / exception handling | Escalate unreviewed grants; auto-revoke per policy on timeout; preserve review evidence. |
| Related records | AccessReview, Permission, User, Role. |
| Required evidence | Review decisions and revocation records. |
| Required approvals | Owner/administrator certification per scope. |
| Audit requirements | Audit review campaigns and outcomes. |
| Metrics produced | Review coverage, revocation rate, and overdue reviews. |
| Configuration options | Review cadence, scope, and auto-revocation policy. |

## Capability: `Custom fields and validation`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-014 |
| Purpose | Define custom fields and validation rules per record type within the common record model. |
| Trigger | Manual / API |
| Primary users | Administrator; Owner |
| Inputs | Record type, field definitions, and validation rules. |
| Outputs | `FieldDefinition` records and validated record metadata. |
| Preconditions | The record type exists; actor holds schema-admin permission. |
| Postconditions | Records of the type validate against the defined fields. |
| Main workflow | Define field (type, required, constraints, classification); attach validation; version the schema; emit audit/event records. |
| Alternate workflows | Import field schema; API update; deprecate field. |
| Error / exception handling | Reject schema changes that invalidate existing records without migration; preserve schema versions. |
| Related records | RecordType, FieldDefinition, Metadata schema. |
| Required evidence | Schema version history. |
| Required approvals | Administrator approval for controlled schema changes. |
| Audit requirements | Audit schema changes. |
| Metrics produced | Schema change frequency and validation-failure rate. |
| Configuration options | Field types, validation library, and schema-versioning policy. |

## Capability: `Record quality checks`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-015 |
| Purpose | Validate record completeness and quality against policy (required fields, classification set, ownership, links). |
| Trigger | Event-driven / Scheduled |
| Primary users | Owner; Reviewer; Administrator; Automation actor |
| Inputs | Records, quality rules, and record type schemas. |
| Outputs | Quality findings, completeness scores, and remediation tasks. |
| Preconditions | Quality rules are configured. |
| Postconditions | Quality gaps are surfaced and actionable. |
| Main workflow | Evaluate records against quality rules; score completeness; flag gaps; emit audit/event records. |
| Alternate workflows | Bulk quality scan; pre-gate quality check; automation-driven remediation suggestion. |
| Error / exception handling | Flag rather than block by default; preserve rule provenance. |
| Related records | RecordType, FieldDefinition; records being checked. |
| Required evidence | Quality findings and scores. |
| Required approvals | None. |
| Audit requirements | Audit quality-rule changes. |
| Metrics produced | Completeness score, gap count, and stale/unowned record count. |
| Configuration options | Quality rule set and scoring weights. |

## Capability: `Retention and legal-hold administration`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-016 |
| Purpose | Administer retention policies and legal holds across record types from the platform admin surface (retention/hold enforcement on evidence/audit is owned by `SPMS-EVID-AUDIT`; this is the admin/config slice). |
| Trigger | Manual / Scheduled / API |
| Primary users | Administrator; Compliance owner; Auditor |
| Inputs | Retention policy definitions, legal-hold orders, classification, and record types. |
| Outputs | Retention/hold configuration, scheduled retention actions, and audit events. |
| Preconditions | Actor holds retention-admin permission. |
| Postconditions | Retention and holds are configured and respected before any deletion/anonymization. |
| Main workflow | Define retention by record type/classification; apply/lift legal holds; schedule retention actions that always honour legal hold and classification; emit audit/event records. |
| Alternate workflows | Bulk policy application; API update; hold from external e-discovery. |
| Error / exception handling | Block deletion under legal hold; require approval for permanent deletion; preserve retention-decision evidence. |
| Related records | RetentionPolicy (`SPMS-EVID-AUDIT`), Legal hold; record types. |
| Required evidence | Retention/hold configuration and action logs. |
| Required approvals | Compliance approval for retention/hold changes. |
| Audit requirements | Audit retention/hold configuration and enforcement. |
| Metrics produced | Records under hold, pending retention actions, and policy coverage. |
| Configuration options | Retention schedules, hold sources, and deletion-approval policy. |

## Capability: `Feature flag management`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-017 |
| Purpose | Manage platform and tenant feature flags that enable/disable capabilities safely. |
| Trigger | Manual / API |
| Primary users | Administrator |
| Inputs | Feature flag definitions, scope (platform/tenant), and default values. |
| Outputs | `FeatureFlag` records and effective flag resolution. |
| Preconditions | Actor holds platform/tenant admin permission. |
| Postconditions | Flags are resolvable per scope and changes are audited. |
| Main workflow | Define flag; set scope/default; override per tenant; resolve effective value; emit audit/event records. |
| Alternate workflows | Gradual rollout; emergency disable; API update. |
| Error / exception handling | Validate flag dependencies; preserve prior values for rollback. |
| Related records | FeatureFlag, SystemSetting, TenantSetting. |
| Required evidence | Flag change history. |
| Required approvals | Administrator approval for production flag changes. |
| Audit requirements | Audit flag changes. |
| Metrics produced | Flag count, override count, and change frequency. |
| Configuration options | Flag scopes, defaults, and rollout strategy. |

## Capability: `Observability and alerting`

| Field | Description |
|---|---|
| Capability ID | SPMS-PLAT-CORE-CAP-018 |
| Purpose | Provide platform health signals, metrics, and alerting (job/queue monitoring, system health) for operations. |
| Trigger | Scheduled / Event-driven |
| Primary users | Administrator; Operator; Auditor; Automation actor |
| Inputs | Health checks, metrics, job/queue state, and alert rules. |
| Outputs | `HealthCheck` and `ObservabilitySignal` records, alerts, and dashboards. |
| Preconditions | Signals are configured. |
| Postconditions | Platform health is observable and alertable. |
| Main workflow | Collect health/metric signals; evaluate alert rules; raise alerts; surface dashboards; emit audit/event records. |
| Alternate workflows | Synthetic checks; on-demand health report; automation-driven remediation. |
| Error / exception handling | Escalate on signal loss; preserve signal provenance. |
| Related records | HealthCheck, ObservabilitySignal, AdminJob. |
| Required evidence | Signal and alert history. |
| Required approvals | None. |
| Audit requirements | Audit alert-rule changes. |
| Metrics produced | Signal coverage, alert volume, and mean-time-to-detect. |
| Configuration options | Signal sources, alert rules, and dashboards. |

---

# 5. Lifecycle and State Model

## 5.1 Managed Object Lifecycle

Primary lifecycle states:

- Draft
- Proposed
- Under Review
- Approved
- Baselined
- Active
- Blocked
- Implemented
- Verified
- Accepted
- Closed
- Deprecated
- Retired
- Archived

## 5.2 State Transition Table

| From state | To state | Trigger | Required conditions | Required approvals | Automatic actions |
|---|---|---|---|---|---|
| Draft | Under Review | Submit for review | Required fields complete; owner assigned. | Owner / reviewer if configured | Notify reviewers; create audit event. |
| Under Review | Approved | Approve | Review comments resolved; evidence complete where required. | Approver role | Lock approved version; emit ApprovalCompleted. |
| Approved | Baselined | Add to baseline | Baseline package complete; no blocking links. | Baseline authority | Create immutable baseline snapshot. |
| Active | Blocked | Blocker detected | Blocking issue, failed gate, dependency, or missing evidence. | None unless policy requires | Notify owner; start SLA/escalation timer. |
| Blocked | Active | Blocker resolved | Blocking condition removed or waived. | Owner / approver as configured | Resume workflow and SLA clock. |
| Active | Closed | Close | Closure criteria met; evidence and approvals present. | Owner / approver | Generate closure audit record; update metrics. |
| Closed | Archived | Retention/archive job | Retention policy permits archive. | Administrator / retention policy | Move to archive state and preserve audit trail. |

## 5.3 Reopen, Rollback, Supersede, and Retirement Rules

Records may be reopened only by authorised roles and only with a reason. Approved or baselined records are superseded rather than silently edited. Rollback restores a previous controlled version while preserving the attempted change and audit trail. Retirement requires ownership review, downstream impact analysis, evidence retention checks, and archive/legal-hold evaluation.

---

# 6. Data Model

## 6.1 Primary Entities

| Entity | Description | Owned by this component? |
|---|---|---|
| Tenant | Primary Platform Core record for tenant management. | Yes |
| Project | Primary Platform Core record for project management. | Yes |
| Product | Primary Platform Core record for product management. | Yes |
| Team | Primary Platform Core record for team management. | Yes |
| User | Primary Platform Core record for user management. | Yes |
| Role | Primary Platform Core record for role management. | Yes |
| Permission | Primary Platform Core record for permission management. | Shared |
| Group | A named collection of users for grant assignment. | Yes |
| ServiceAccount | A non-human automation identity with scoped, expiring authority. | Yes |
| Delegation | A time-bounded, scoped delegation of authority between identities. | Yes |
| AccessReview | A recertification campaign over access grants. | Yes |
| RecordType | A component-defined record type within the common record model. | Yes |
| FieldDefinition | A custom field definition and its validation rules for a record type. | Yes |
| ClassificationLabel | A classification label governing access, export, retention, and AI retrieval. | Yes |
| LifecycleState | A configured lifecycle state mapped to the canonical state set. | Yes |
| SystemSetting | A platform-scoped administrative setting. | Yes |
| TenantSetting | A tenant-scoped administrative setting. | Yes |
| FeatureFlag | A platform/tenant feature flag. | Yes |
| HealthCheck | A platform health probe and its latest result. | Yes |
| ObservabilitySignal | A metric/log/trace signal used for monitoring and alerting. | Yes |
| AdminJob | A background/administrative job with monitored state. | Yes |
| Metadata schema | Primary Platform Core record for metadata schema management. | Shared |
| Taxonomy | Primary Platform Core record for taxonomy management. | Shared |
| Workspace | Primary Platform Core record for workspace management. | Shared |

The concrete `User`, `Role`, and `Permission` schemas are defined in `SPMS-DOMAIN-MODEL` §7.2 and
referenced here; the management entities above (RecordType, FieldDefinition, ClassificationLabel,
LifecycleState, and the admin/observability entities) are Platform Core's owned configuration
entities. `RetentionPolicy` and `LegalHold` are owned by `SPMS-EVID-AUDIT` and referenced, not
redefined, here.

## 6.2 Entity Attributes

## Entity: `Tenant`

| Attribute | Type | Required? | Description | Validation rules |
|---|---|---|---|---|
| ID | UUID / String | Yes | Stable unique identifier. | Immutable; globally unique within tenant. |
| Name / title | String | Yes | Human-readable name. | Unique where required by project or component policy. |
| Status | Enum | Yes | Lifecycle state. | Must match component state model. |
| Owner | User / Team / Role | Yes | Accountable owner. | Must resolve to active identity or role. |
| Project / product scope | Reference | Conditional | Owning project, product, tenant, or workspace. | Required unless global substrate object. |
| Classification | Enum | Conditional | Data/security/business classification. | Must use platform classification taxonomy. |
| Version | String / Integer | Yes | Current version or revision. | System managed for controlled records. |
| Created at / by | DateTime + Actor | Yes | Creation metadata. | System generated. |
| Updated at / by | DateTime + Actor | Yes | Last update metadata. | System generated. |
| Tags / metadata | Map | No | Extensible module metadata. | Validated by metadata schema. |

## Entity: `ServiceAccount`

| Attribute | Type | Required? | Description | Validation rules |
|---|---|---|---|---|
| ID | UUID / String | Yes | Stable unique identifier. | Immutable; globally unique within tenant. |
| Name | String | Yes | Human-readable name. | Unique within tenant. |
| Owner | User / Team / Role | Yes | Accountable human owner. | Must resolve to active identity. |
| Purpose | String | Yes | Why the account exists. | — |
| Scope | List of references | Yes | The components/projects/actions the account may perform. | Least-privilege; validated on use. |
| Expiry | DateTime | Yes | When the account/credential expires. | Must be set; renewal required. |
| Secret refs | List of references | No | Credentials referenced by the account. | References only; never raw secret values. |
| Status | Enum | Yes | One of: active, suspended, expired, revoked. | — |
| Created at / by | DateTime + Actor | Yes | Creation metadata. | System generated. |

## Entity: `Delegation`

| Attribute | Type | Required? | Description | Validation rules |
|---|---|---|---|---|
| ID | UUID / String | Yes | Stable unique identifier. | Immutable; globally unique within tenant. |
| Delegator | Reference | Yes | The identity delegating authority. | Must hold the delegated authority. |
| Delegate | Reference | Yes | The identity receiving authority. | Must be an eligible identity. |
| Scope | List of references | Yes | The authority/actions delegated. | Cannot exceed the delegator's authority. |
| Starts at / Expires at | DateTime | Yes | Validity window. | Time-bounded; expiry required. |
| Status | Enum | Yes | One of: active, expired, revoked. | — |
| Created at / by | DateTime + Actor | Yes | Creation metadata. | System generated. |

## Entity: `FieldDefinition`

| Attribute | Type | Required? | Description | Validation rules |
|---|---|---|---|---|
| ID | UUID / String | Yes | Stable unique identifier. | Immutable; globally unique within tenant. |
| Record type | Reference | Yes | The record type this field belongs to. | Must resolve to a registered `RecordType`. |
| Name / key | String | Yes | Field key. | Unique within the record type. |
| Data type | Enum | Yes | Field data type. | One of: string, number, boolean, date, enum, reference, list. |
| Required | Boolean | Yes | Whether the field is mandatory. | — |
| Constraints | Structured | No | Validation constraints (range, pattern, enum values). | Validated on record write. |
| Classification | Enum | Conditional | Field-level classification for field security. | Must use platform classification taxonomy. |
| Schema version | Integer | Yes | Version of the field schema. | Incremented on controlled change. |

## Entity: `FeatureFlag`

| Attribute | Type | Required? | Description | Validation rules |
|---|---|---|---|---|
| ID | UUID / String | Yes | Stable unique identifier. | Immutable; globally unique within tenant. |
| Key | String | Yes | Flag key. | Unique within scope. |
| Scope | Enum | Yes | One of: platform, tenant. | — |
| Default value | Boolean / Enum | Yes | Default flag value. | — |
| Tenant overrides | Map | No | Per-tenant override values. | Only for platform-scope flags. |
| Status | Enum | Yes | One of: active, deprecated. | — |
| Created at / by | DateTime + Actor | Yes | Creation metadata. | System generated. |

## 6.3 Relationships

| Relationship | Source entity | Target entity | Cardinality | Required? | Description |
|---|---|---|---|---|---|
| owns | Team / User / Role | Record | 1:N | Yes | Defines accountability. |
| linked-to | Record | Record | N:N | No | General relationship for related records. |
| evidenced-by | Record | Evidence | N:N | Conditional | Connects claims, decisions, results, and approvals to proof. |
| approved-by | Record | Approval | N:N | Conditional | Formal approval and sign-off. |
| included-in | Record | Baseline / Release / Work Package | N:N | Conditional | Scope, baseline, release, or package membership. |
| verifies | Test / Evidence | Requirement | N:N | Conditional | Verification coverage. |
| affects | Risk / Vulnerability / Change | Asset / Release / Requirement | N:N | Conditional | Impact and risk propagation. |

## 6.4 Applicability and Variants

Records must support applicability by project, product, release, customer, tenant, environment, platform, region, configuration, variant, and governance profile. Applicability is inherited from parent records unless overridden by controlled variant rules.

---

# 7. Traceability and Impact Analysis

## 7.1 Required Trace Links

| Link type | Required when | Source | Target | Purpose |
|---|---|---|---|---|
| derives-from | When a record is based on a source, parent, standard, or decision. | Current record | Source record | Preserve rationale and origin. |
| implements | When work, build, release, or asset satisfies a planned item. | Implementation object | Requirement / issue / work package | Show delivery coverage. |
| verifies | When evidence proves a requirement, control, issue, or gate. | Test / evidence | Requirement / control / gate | Show verification. |
| evidenced-by | When decisions or states require proof. | Controlled record | Evidence item | Support audit and acceptance. |
| approved-by | When approval is required. | Controlled record | Approval record | Accountable governance. |
| deployed-to | When software/configuration is installed. | Release / artifact / component | Environment / asset | Deployment inventory. |
| affects | When change, risk, vulnerability, or drift has impact. | Change / risk / finding | Affected object | Impact analysis. |
| mitigates | When action or control reduces risk/finding. | Action / control | Risk / vulnerability / NCR | Assurance and security trace. |

## 7.2 Coverage Rules

- Every controlled record must have an owner, status, history, and project/tenant scope.
- Every approved or baselined record must trace to its approval and evidence where evidence is required.
- Every release, gate, audit, waiver, and acceptance decision must trace to included scope, evidence, approvals, and exceptions.
- Every downstream record must be marked suspect when an upstream approved record changes.

## 7.3 Impact Analysis Rules

| Change event | Impact analysis required |
|---|---|
| Record modified after approval | Mark downstream links suspect; require reapproval or justification. |
| Requirement changed | Identify affected designs, tests, code, work packages, releases, evidence, waivers. |
| Asset or environment changed | Identify affected services, deployments, tests, vulnerabilities, releases, operational docs. |
| Evidence expires or becomes stale | Identify affected gates, releases, audits, acceptance decisions, controls. |
| Workflow or policy changed | Identify active records whose lifecycle or approval requirements are affected. |

---

# 8. Governance, Approvals, Waivers, and Gates

## 8.1 Governance Profile Support

| Governance profile | Description | Typical use |
|---|---|---|
| Lightweight | Minimal review and evidence. | Small internal project. |
| Low-risk bulk | Automated rule-based approval for bulk, low-risk items (e.g. minor metadata updates) when all integrity checks pass; full audit trail maintained; escalates to Standard on any check failure. | Bulk metadata corrections, tag updates, minor field amendments. |
| Standard | Normal review, approval, and evidence. | Typical product/project. |
| Controlled | Formal baselines, approvals, evidence, audit. | Customer, regulated, or high-risk work. |
| Critical | Strong separation of duties, independent assurance, strict gates. | Security/safety/business-critical systems. |

## 8.2 Approval Rules

| Approval type | Required for | Approver role | Expiry / reapproval rule |
|---|---|---|---|
| Owner approval | Controlled state changes and closure. | Record owner | Required again after material change. |
| Technical approval | Technical content, implementation, configuration, or topology. | Technical authority | Expires when affected technical content changes. |
| Architecture approval | Architecture-significant records or changes. | Architect / design authority | Required again after architecture-impacting change. |
| Security approval | Security-sensitive records, exceptions, releases, vulnerabilities. | Security authority | Expires at risk/exception expiry or scope change. |
| Product approval | Scope, priority, acceptance, and release decisions. | Product owner | Required for scope change. |
| Customer approval | Customer-facing baselines, waivers, releases, or acceptance. | Customer authority | Required if customer obligation changes. |
| PA / QA approval | Assurance gates, NCRs, waivers, acceptance packages. | PA / QA authority | Required after evidence or scope changes. |
| Baseline approval | Creation or revision of official baselines. | Baseline authority | Required for each baseline revision. |
| Acceptance approval | Final acceptance or closure. | Acceptance authority | Required after failed validation or reopened item. |

## 8.3 Gate Rules

| Gate | Required evidence | Blocking conditions | Approvers |
|---|---|---|---|
| Intake gate | Required fields, owner, classification, initial links. | Missing owner/scope/classification. | Owner / triage role. |
| Baseline gate | Approved scope, resolved review comments, complete links. | Unresolved changes or missing approvals. | Baseline authority. |
| Architecture gate | Design record, impact analysis, risks, decisions. | Architecture-significant unresolved issues. | Architecture authority. |
| Implementation gate | Accepted plan, linked work, build/test path. | Missing implementation trace or policy violations. | Technical lead / owner. |
| Test readiness gate | Test scope, environment, data, entry criteria. | Missing test assets or environment readiness. | Test authority. |
| Release readiness gate | Tests, scans, docs, evidence, operations readiness. | Failed tests, missing evidence, open blockers. | Release board. |
| Security gate | Scans, threat review, vulnerabilities, privacy review. | Unaccepted critical security risk. | Security authority. |
| Deployment gate | Approved window, plan, rollback, environment checks. | Unapproved deployment or unavailable rollback. | Deployment authority. |
| Acceptance gate | Verification, validation, waivers, customer/product sign-off. | Unverified scope or missing acceptance evidence. | Acceptance authority. |
| Closure gate | All actions complete, evidence archived, lessons captured. | Open required actions or missing audit history. | Owner / PA as configured. |

## 8.4 Waivers, Deviations, and Exceptions

| Field | Requirement |
|---|---|
| Waiver ID | System-generated stable identifier. |
| Affected object | Must link to affected record, baseline, release, requirement, control, asset, or evidence. |
| Reason | Business and technical rationale required. |
| Impact analysis | Must identify downstream impact and residual risk. |
| Risk assessment | Severity, likelihood, owner, residual risk, and review cadence. |
| Compensating controls | Required when risk remains active. |
| Expiry date | Required unless explicitly approved as permanent. |
| Required approvers | Owner plus specialist/governance authority based on profile. |
| Renewal rules | Renewal requires fresh impact analysis and approval. |
| Closure rules | Close when remediated, superseded, expired, or formally retired. |

---

# 9. Evidence, Audit, and Historical Reconstruction

## 9.1 Evidence Requirements

| Evidence type | Required for | Source | Retention rule |
|---|---|---|---|
| Approval record | Controlled transitions, gates, baselines, waivers, acceptance. | Workflow engine | Retain for object lifetime plus policy period. |
| Test result | Verification, validation, release readiness. | Test system / CI/CD | Retain with release/baseline evidence. |
| Build log | Build, artifact, provenance, reproducibility. | Pipeline system | Retain per pipeline/release policy. |
| Scan report | Security, compliance, supply-chain gates. | Security tool / CI/CD | Retain per compliance policy. |
| Review record | Document, requirement, design, PA, gate reviews. | Document / PA system | Retain with controlled record. |
| Deployment log | Deployment execution and rollback decisions. | Release / deployment system | Retain with deployment record. |
| Decision record | Rationale for controlled choices. | Knowledge system | Retain with linked records. |
| Configuration snapshot | Baseline, test, release, audit reconstruction. | Asset/config system | Retain with baseline/release/audit. |

## 9.2 Evidence Metadata

Each evidence item should include: Evidence ID, evidence type, source system, owner, creation date, related object, related version/baseline, related environment, related build/release/deployment, review status, approval status, expiry/freshness rule, integrity hash, and retention rule.

## 9.3 Audit Events

| Event | Must be audited? | Notes |
|---|---|---|
| Create record | Yes | Include actor, source, initial fields. |
| Modify record | Yes | Include before/after diff. |
| Delete / archive record | Yes | Prefer soft delete and preserve references. |
| Approve / reject | Yes | Include approver, role, rationale. |
| Baseline | Yes | Include full included set and versions. |
| Waiver / exception | Yes | Include rationale, risk, expiry, approvers. |
| Evidence upload | Yes | Include hash, source, provenance, object reference. |
| Permission change | Yes | Access-sensitive. |
| Export | Yes | Especially evidence/audit exports. |
| Integration update | Yes | Include actor/system and payload summary. |

## 9.4 Historical Reconstruction

The component must support reconstruction of state at a specific date/time, named baseline, release approval, deployment, audit period, acceptance, and before/after a change. Reconstruction must include records, relationships, workflow state, approvals, evidence metadata, and relevant immutable audit events.

---

# 10. Search, Views, Dashboards, and Reporting

## 10.1 Search Requirements

| Search type | Required? | Description |
|---|---|---|
| Full-text search | Yes | Search titles, descriptions, comments, documents, logs, attachments, and evidence metadata. |
| Structured filtering | Yes | Filter by fields, status, owner, project, product, release, environment, risk, dates. |
| Advanced query language | Yes | Query records, relationships, baselines, and evidence. |
| Graph navigation | Yes | Traverse dependencies, trace links, topology, and impact paths. |
| Semantic search | Yes | Find conceptually related knowledge and controlled records. |
| Natural-language Q&A | Yes | Must cite approved source records and respect permissions. |

## 10.2 Standard Views

| View | Users | Purpose |
|---|---|---|
| List view | All users | Browse and filter records. |
| Detail view | All users | Inspect one record, metadata, links, evidence, comments, history. |
| Board view | Contributors / owners | Manage lifecycle queues where applicable. |
| Matrix view | Reviewers / auditors | Show coverage and cross-object status. |
| Graph view | Engineers / assurance / auditors | Explore dependencies, topology, and impact. |
| Timeline view | Managers / owners | Show schedule, state history, and planned events. |
| Calendar view | Teams / approvers | Show deadlines, gates, SLAs, reviews. |
| Dashboard view | Managers / executives | Show operational and strategic metrics. |
| Audit view | Auditors / governance | Show immutable history, evidence, approvals, exports. |

## 10.3 Reports and Metrics

| Metric / report | Description | Frequency | Audience |
|---|---|---|---|
| Inventory report | Record counts, ownership, status, classifications, stale/unowned items. | On demand / scheduled | Owners / administrators. |
| Status report | Progress, blockers, approvals, SLAs, exceptions. | Weekly / on demand | Teams / managers. |
| Coverage report | Traceability and evidence coverage. | Gate / baseline / on demand | Reviewers / assurance. |
| Readiness report | Gate, release, acceptance, or closure readiness. | At gates | Approvers / boards. |
| Evidence completeness report | Missing, stale, unreviewed, or invalid evidence. | Scheduled / at gates | Owners / auditors. |
| Risk report | Open risks, exceptions, high-impact items, overdue actions. | Weekly / monthly | Governance. |
| Audit report | Historical state, approvals, changes, evidence packages. | Audit period / on demand | Auditors. |
| Trend report | Throughput, cycle time, quality, security, cost, reliability trends. | Monthly / quarterly | Executives / portfolio. |

---

# 11. Automation, Events, and AI Assistance

## 11.1 Events Produced

| Event | Trigger | Payload summary | Consumers |
|---|---|---|---|
| RecordCreated | New record created | Record ID, type, scope, owner, source | Workflow, reporting, notifications. |
| RecordUpdated | Record changed | Changed fields, actor, old/new values, version | Traceability, audit, automation. |
| StateChanged | Lifecycle transition | From/to state, reason, actor | Notifications, metrics, SLA. |
| ApprovalRequested | Approval needed | Approver role, due date, record, gate | Approver queues, reminders. |
| ApprovalCompleted | Approval/rejection completed | Decision, approver, rationale | Audit, gate engine. |
| EvidenceAdded | Evidence linked/uploaded | Evidence ID, record ID, hash, source | Evidence completeness, audit. |
| BaselineCreated | Baseline snapshot created | Baseline ID, included objects, versions | Traceability, reporting. |
| GateFailed | Gate check failed | Gate, blocking conditions, missing items | Notifications, issue creation. |
| WaiverCreated | Waiver/deviation created | Waiver ID, affected object, expiry | Risk, reporting, reminders. |
| RecordClosed | Record closed | Closure state, evidence, approver | Reporting, archive policies. |

## 11.2 Events Consumed

| Event | Source | Action taken |
|---|---|---|
| IdentityChanged | Platform Core | Refresh permissions, ownership, delegation, and audit access. |
| PolicyChanged | Workflow & Governance Core / Automation | Recalculate gates, approvals, and compliance expectations. |
| LinkChanged | Traceability Graph Core | Recalculate coverage and suspect links. |
| EvidenceStale | Evidence & Audit Core | Mark affected records, gates, and reports as requiring review. |
| BuildTestScanCompleted | CI/CD / Test / Security | Update readiness, evidence, coverage, and blockers. |

## 11.3 Automation Rules

| Rule | Trigger | Conditions | Actions |
|---|---|---|---|
| Auto-assignment | RecordCreated | Owner/component/team rules match | Assign owner, watchers, and SLA. |
| Evidence completeness check | StateChanged / scheduled | Record approaches gate or review date | Flag missing evidence; notify owner. |
| Stale record escalation | Scheduled | Record inactive or overdue | Notify owner; escalate to manager/board. |
| Suspect link propagation | RecordUpdated | Approved upstream record changed | Mark downstream links suspect. |
| Gate enforcement | ApprovalRequested / StateChanged | Blocking conditions exist | Prevent transition and create blockers. |

## 11.4 AI-Assisted Functions

| AI function | Allowed? | Human approval required? | Notes |
|---|---|---|---|
| Summarization | Yes | No | Summarize records, evidence, comments, logs, and reports. |
| Draft generation | Yes | Yes | Draft records, reports, decisions, release notes, test cases, or responses. |
| Classification suggestion | Yes | Yes / No | Suggest types, severity, priority, owners, controls, tags. |
| Duplicate detection | Yes | No | Find similar records and propose merge/link options. |
| Traceability suggestion | Yes | Yes | Suggest links but do not create controlled links silently. |
| Impact analysis assistance | Yes | Yes | Summarize likely impact from graph and evidence. |
| Evidence gap detection | Yes | No / Yes | Identify missing, stale, or weak evidence. |
| Natural-language Q&A | Yes | No | Must cite sources and respect permissions. |
| Automated approval | No | Not allowed | AI must not approve controlled records. |

---

# 12. Integrations and APIs

## 12.1 External Integrations

| System | Integration type | Direction | Data exchanged |
|---|---|---|---|
| Git provider | API / Webhook | Inbound / Outbound | Branches, commits, pull requests, reviews, files, tags. |
| CI/CD platform | API / Webhook | Inbound / Outbound | Builds, tests, scans, artifacts, deployments, logs. |
| Artifact repository | API | Inbound / Outbound | Packages, containers, binaries, SBOMs, signatures. |
| Test framework | Import / API | Inbound | Test results, coverage, reports, evidence. |
| Security scanner | Import / API | Inbound | Vulnerabilities, findings, SBOMs, scan reports. |
| Monitoring system | Webhook / API | Inbound | Alerts, health, metrics, deployment impact. |
| Identity provider | OIDC / SAML / LDAP | Inbound | Users, groups, roles, authentication. |
| Document repository | API / Import / Export | Inbound / Outbound | Documents, decisions, reports, knowledge. |
| ITSM system | API | Inbound / Outbound | Incidents, changes, requests, approvals. |
| Cloud provider | API | Inbound | Assets, environments, IAM, configuration, posture. |

## 12.2 Public APIs

| API | Purpose | Auth model | Notes |
|---|---|---|---|
| Create record | Create a scoped module record. | User token / service token with create permission. | Validates schema and workflow. |
| Update record | Update editable fields and metadata. | User/service token with edit permission. | Creates diff and audit event. |
| Query records | Search and filter records. | Permission-filtered auth. | Supports pagination and saved views. |
| Create link | Create typed traceability link. | Link permission and policy validation. | May require approval for controlled links. |
| Upload evidence | Register or attach evidence. | Evidence upload permission. | Stores hash/provenance. |
| Request approval | Start approval workflow. | Workflow permission. | Uses governance profile. |
| Export package | Export records, evidence, or audit package. | Export permission and audit logging. | May require approval for sensitive exports. |

## 12.3 Import / Export

| Format | Import | Export | Notes |
|---|---|---|---|
| CSV | Yes | Yes | Flat records and reporting exports. |
| Excel | Yes | Yes | Bulk import/export for controlled migration and review. |
| JSON | Yes | Yes | API and structured package exchange. |
| XML | Yes | Yes | Enterprise integration and legacy import. |
| YAML | Yes | Yes | Configuration-as-code and pipeline/policy definitions. |
| Markdown | Yes | Yes | Documentation, reports, specs, and knowledge records. |
| PDF | Conditional | Yes | Document/evidence export; import metadata/text where possible. |
| Word | Conditional | Yes | Controlled document migration and export. |
| ReqIF | Conditional | Conditional | Requirements-specific where applicable. |
| ZIP evidence package | Yes | Yes | Evidence, audit, release, acceptance, or compliance package. |

---

# 13. Security, Privacy, and Compliance Requirements

## 13.1 Access Control

| Object / action | Permission required |
|---|---|
| View record | Read permission on tenant/project/object and classification. |
| Create record | Create permission for component and scope. |
| Edit record | Edit permission, valid workflow state, no lock violation. |
| Approve record | Approver role and SoD validation. |
| Delete / archive record | Admin/owner authority plus retention policy compliance. |
| Export record | Export permission; sensitive exports may require approval. |
| View evidence | Evidence permission and classification access. |
| Upload evidence | Evidence upload permission and malware/content validation. |
| Change permissions | Administrator or delegated permission manager. |
| Configure workflow | Component administrator and governance authority. |

### 13.1.1 RBAC, ABAC, and Field-Level Rules

Effective authorization (CAP-009/010) is resolved by combining role grants with attribute-based
rules, applying a fixed inheritance order from most general to most specific, where the most
specific applicable rule wins:

`tenant → project/product → team → object (record) → field/action override`

- **RBAC:** grants are assigned to users, teams, groups, roles, or service accounts at a scope
  (tenant/project/component).
- **ABAC:** when a role grant alone is insufficient, the decision evaluates attributes — the
  principal's `classification_clearance` vs the target `classification`, project/team membership,
  the record/project `governance_profile`, and the record `lifecycle_state` (e.g. baselined records
  are read-only outside a change request).
- **Object- and field-level overrides** may further **restrict** (never broaden) access; a
  field-level override can hide or block individual fields even when the record is otherwise
  readable. Conflicts resolve to the most restrictive outcome; ambiguity defaults to deny.
- **Service accounts** must have an owner, purpose, least-privilege scope, expiry, and a full audit
  trail. **Delegated authority** is time-bounded, scoped, visible in approval records, and never
  erases the original authority. Detailed security architecture and ABAC/RBAC evaluation are
  governed by `SPMS-STD-SEC`; the canonical authorization model is in `SPMS-DOMAIN-MODEL` §7.2.

## 13.2 Data Classification

Supported classifications: Public, Internal, Confidential, Restricted, Customer-confidential, Security-sensitive, Personal data, Regulated data, Export-controlled.

## 13.3 Privacy Requirements

| Data type | Yes / No | Controls |
|---|---|---|
| Personal data | Conditional | Minimize fields, classify, protect exports, retention rules, audit access. |
| Customer data | Conditional | Tenant/customer isolation, contractual retention, access controls. |
| Security-sensitive data | Conditional | Restrict access, redact secrets, protect evidence and scan reports. |
| Regulated data | Conditional | Apply controls, retention, legal hold, audit exports. |

## 13.4 Compliance Requirements

| Requirement | Description |
|---|---|
| Auditability | All controlled actions must be immutable and attributable. |
| Retention | Retention policies must be configurable per object type and classification. |
| Legal hold | Records and evidence under legal hold must not be deleted or modified silently. |
| Encryption | Encrypt data in transit and at rest, including object storage and backups. |
| Export control | Restrict export-controlled records by user, region, tenant, and classification. |
| Segregation of duties | Enforce incompatible role combinations for controlled approvals. |

---

# 14. Configuration and Administration

## 14.1 Configurable Elements

| Element | Configuration need |
|---|---|
| Workflow states and transitions | Lifecycle model, validators, actions, notifications. |
| Fields and schemas | Required fields, custom fields, metadata validation. |
| Roles and permissions | RBAC/ABAC rules, project and object access, delegation. |
| Gate rules | Criteria, evidence, approvals, blockers, revalidation. |
| Notification schemes | Recipients, triggers, escalation, digests, chat/webhooks. |
| Retention policies | Archive, delete, legal hold, evidence retention. |
| Import/export mappings | Field mapping, ID mapping, validation, duplicate detection. |
| Automation rules | Triggers, conditions, actions, policy-as-code bundles. |

## 14.2 Governance Profiles

Lightweight minimizes approvals and evidence; Standard uses normal review and approval; Controlled requires formal baselines, evidence, waivers, and audit trails; Critical adds independent assurance, stricter SoD, mandatory gates, and stronger retention.

## 14.3 Feature Flags

| Feature | Default | Description |
|---|---|---|
| Advanced graph analysis | On | Enable graph traversal, impact analysis, and matrices. |
| AI assistance | On | Enable governed AI suggestions and Q&A. |
| External collaborator access | Off | Enable controlled customer/supplier/auditor access. |
| Strict SoD enforcement | On for controlled/critical | Prevent requester/approver conflicts. |
| Bulk import | On | Allow governed imports with validation and rollback. |

---

# 15. Non-Functional Requirements

## 15.1 Performance

| Requirement | Target |
|---|---|
| Page load time | P95 under 2 seconds for standard record views at target scale. |
| Search response time | P95 under 2 seconds for indexed queries. |
| Graph query response time | P95 under 5 seconds for bounded impact queries. |
| Import throughput | At least 10,000 records/hour with validation in standard deployments. |
| Export generation time | Audit packages generated asynchronously for large exports. |
| Event processing latency | P95 under 60 seconds for normal workflow events. |

## 15.2 Scalability

Define expected scale for number of tenants, projects, users, records, relationships, evidence files, events per day, integrations, and concurrent users. The component must support single-project/single-team operation without requiring portfolio structures, and multi-project/multi-team operation through configuration, indexing, graph projections, workers, and partitioning.

## 15.3 Availability and Resilience

| Requirement | Target |
|---|---|
| Availability | Target 99.5% or higher for standard deployments; higher for critical deployments. |
| RPO | Configurable; target less than 15 minutes for core data. |
| RTO | Configurable; target less than 4 hours for standard deployments. |
| Backup frequency | Daily full plus continuous/near-continuous event/object metadata protection. |
| Restore test frequency | At least quarterly for governed deployments. |
| Degraded mode behavior | Read-only mode for controlled records if write dependencies are unavailable. |

## 15.4 Usability and Accessibility

Include keyboard navigation, screen reader compatibility, responsive UI, localization, time zone support, bulk operations, saved views, command palette, and role-specific dashboards.

## 15.5 Maintainability

Maintain modular boundaries, versioned APIs, migration support, high automated test coverage, configuration-as-code where applicable, observability, and administrator/user documentation.

---

# 16. User Interface Requirements

## 16.1 Primary Screens

| Screen | Purpose | Users |
|---|---|---|
| List / queue | Browse, search, triage, and bulk manage records. | Contributors, owners, reviewers. |
| Detail page | View record fields, links, evidence, comments, approvals, audit. | All permitted users. |
| Create/edit form | Create or update records with validation and templates. | Contributors, owners. |
| Review page | Review comments, diffs, evidence, and findings. | Reviewers. |
| Approval page | Approve/reject with rationale and conditions. | Approvers. |
| Graph / traceability view | Explore links, topology, impact, and matrices. | Engineers, assurance, auditors. |
| Dashboard | Show metrics, status, readiness, risk, trends. | Managers, executives, teams. |
| Audit history | Inspect immutable changes, approvals, evidence, exports. | Auditors, administrators. |
| Configuration page | Manage schemas, workflows, policies, integrations. | Administrators. |

## 16.2 Common UI Patterns

The component should support saved filters, bulk selection, inline editing where safe, comment threads, activity feed, attachments/evidence panel, relationship panel, approval panel, audit history panel, export action, status badges, risk/priority/severity indicators, and warnings for missing evidence or broken traceability.

---

# 17. Migration, Import, and Backward Compatibility

## 17.1 Migration Sources

| Source | Data to migrate | Notes |
|---|---|---|
| Spreadsheet | Records, fields, relationships, assignments. | Validate schema and duplicates. |
| Existing tracker | Issues, tasks, changes, workflow states, comments. | Preserve IDs where possible. |
| Document repository | Documents, versions, metadata, approvals. | Import as controlled documents where needed. |
| Git repository | Code links, docs-as-code, configs, history references. | Do not import raw secrets. |
| CI/CD platform | Builds, logs, artifacts, pipeline history. | Import metadata and evidence references. |
| Security scanner | Findings, vulnerabilities, reports. | Normalize severity and asset mappings. |
| CMDB / asset tool | Assets, environments, relationships. | Reconcile duplicates and ownership. |

## 17.2 Migration Rules

Define ID mapping, duplicate detection, field mapping, relationship mapping, attachment migration, evidence migration, audit history preservation, validation before import, import error handling, and rollback strategy. All imports must produce audit events and import validation reports.

## 17.3 Backward Compatibility

Maintain compatibility for APIs, data exports, workflow definitions, plugin interfaces, baselines, historical records, and audit packages. Breaking changes require migration tooling, communication, and rollback or compatibility windows.

---

# 18. Testing and Acceptance Criteria

## 18.1 Test Scope

The component must be tested for schema validation, workflows, approvals, SoD, gates, waivers, evidence handling, audit immutability, traceability, search, reporting, import/export, permissions, API behavior, performance, migration, backup/restore, and integration failure modes.

## 18.2 Acceptance Criteria

| ID | Acceptance criterion |
|---|---|
| AC-001 | All template sections are implemented and configured for the component. |
| AC-002 | Core lifecycle, approval, evidence, traceability, audit, search, and reporting functions work end-to-end. |
| AC-003 | Permissions, tenant/project isolation, SoD, and classification rules are enforced. |
| AC-004 | Historical reconstruction works for records, baselines, approvals, evidence, and changes. |
| AC-005 | Import/export, APIs, automation events, and integrations meet defined contracts. |

## 18.3 Definition of Done

- Functional capabilities implemented and tested.
- Data model, APIs, events, permissions, and workflows documented.
- UI views, dashboards, reports, and configuration screens available.
- Evidence, audit, and historical reconstruction validated.
- Migration/import/export paths tested.
- Operational monitoring, backup, restore, and administration documented.

---

# 19. Operational Requirements

## 19.1 Monitoring

Monitor request latency, error rates, background jobs, event processing, integration health, indexing lag, graph projection lag, evidence storage health, export jobs, import jobs, permission errors, gate failures, and AI/automation tool usage.

## 19.2 Administration

Administrators require tenant/project configuration, schemas, workflows, roles, permissions, retention, integration settings, import/export jobs, feature flags, operational health, audit exports, and support diagnostics.

## 19.3 Backup, Restore, and Archival

Back up relational records, graph projections, search indexes or rebuild sources, object storage, audit/event logs, configuration, and encryption metadata. Restore procedures must be tested and must preserve immutable audit history and evidence integrity.

---

# 20. Open Questions, Assumptions, and Risks

## 20.1 Assumptions

| ID | Assumption | Impact if false |
|---|---|---|
| A-001 | The platform provides common identity, tenant/project scoping, permissions, metadata, audit, and evidence services. | If false, each module will duplicate foundational behavior and lose consistency. |
| A-002 | Governance profiles can be configured per tenant/project/product/environment. | If false, modules may be either too heavy or too weak for different contexts. |
| A-003 | External integrations may be unavailable or partial during initial deployment. | Import/export and manual fallback paths must be available. |

## 20.2 Open Questions

| ID | Question | Owner | Decision needed by |
|---|---|---|---|
| Q-001 | Which governance profiles are enabled for the first release? | Product / governance owner | Before implementation planning. |
| Q-002 | Which external tools are authoritative sources for initial migration? | System owner | Before migration design. |
| Q-003 | What retention periods apply by classification and customer/contract? | Compliance owner | Before production deployment. |

## 20.3 Risks

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R-001 | Over-customization of workflows and fields. | Hard-to-maintain configurations and inconsistent reporting. | Provide governance templates and configuration review. |
| R-002 | Incomplete traceability or evidence migration. | Weak auditability and readiness decisions. | Run migration validation and gap reports. |
| R-003 | Automation acts without sufficient human oversight. | Incorrect controlled decisions or compliance risk. | Disallow automated approvals and require review for controlled suggestions. |

---

# 21. Implementation Notes

## 21.1 Suggested Implementation Approach

Implement as a shared internal service / platform substrate with APIs and projections. Use the common event bus, shared metadata model, workflow/gate engine, traceability graph, evidence repository, and audit log from the foundation.

## 21.2 Data Ownership

| Data | Owner component | Read by | Written by |
|---|---|---|---|
| Tenant | Platform Core | Related modules, reporting, traceability, audit | This component and authorised imports |
| Trace links | Traceability Graph Core | Platform Core, reporting, assurance, AI | This component via graph API |
| Evidence metadata | Evidence & Audit Core | Platform Core, audit, reporting | Evidence service and authorised actors |
| Approval records | Workflow & Governance Core | Platform Core, audit, reporting | Workflow service |

## 21.3 Extension Points

| Extension point | Purpose |
|---|---|
| Workflow extension | Add lifecycle states, transitions, validators, actions. |
| Field extension | Add custom fields and validation rules. |
| Rule extension | Add trigger-condition-action automation and policy-as-code. |
| Integration adapter | Connect external tools, imports, webhooks, and APIs. |
| Report extension | Add dashboards, metrics, exports, and analytic views. |
| AI tool extension | Add grounded summarization, classification, trace suggestions, and Q&A. |
| Import/export adapter | Support additional formats and legacy systems. |

---

# 22. Appendix: Component-Specific Addendum

## 22.1 Source Coverage Checklist

This specification covers the requested module scope: Tenant and workspace management, Project/product/team registry, Identity and access management, Metadata and taxonomy management, Common object model, Notification and activity substrate, Administration console, Platform operations and resilience, RBAC and ABAC authorization, Object and field-level permissions, Approval authority and delegation, Separation of duties, Access review and evidence, Custom fields and validation, Record quality checks, Retention and legal-hold administration, Feature flag management, Observability and alerting.

## 22.2 Specialized Rules

- Tenant isolation and project/product/team hierarchy are mandatory foundations.
- Identity must support SSO/OIDC/SAML/LDAP, local identities where configured, groups, service accounts, and external collaborators.
- Permission model must support RBAC, ABAC, object-level rules, field restrictions, and classification-aware access, resolved in the fixed inheritance order tenant → project/product → team → object → field/action override (see §13.1.1); the most specific applicable rule wins and ambiguity defaults to deny.
- Service accounts must have an owner, purpose, least-privilege scope, and expiry; delegated authority is time-bounded, scoped, and never erases the original authority.
- Record identifiers are immutable and independent of title, location, and hierarchy; classification labels drive permissions, export, retention, AI retrieval, and external sharing; the common lifecycle allows module-specific states without breaking cross-module reporting.
- Metadata schema and taxonomy services must be common across modules for consistent reporting and search.
- Administrative and security-sensitive actions are always audited; retention actions must respect legal hold and classification before any deletion or anonymization (retention/hold enforcement on evidence and audit is owned by `SPMS-EVID-AUDIT`).
- Security architecture, tenant isolation model, ABAC/RBAC evaluation order, field-level security, service identity, secret-reference handling, audit log tamper resistance, export-control enforcement, and AI retrieval permission boundaries are governed by `SPMS-STD-SEC`.
- Configuration governance — the taxonomy of fixed, canonical-constrained, and free configuration surfaces, consistency guardrails, and tenant divergence prevention — is governed by `SPMS-STD-CONFIG`.
