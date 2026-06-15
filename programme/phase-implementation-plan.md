# Phase Implementation Plan — Modular Software Project Management System

## Document Control

| Field | Value |
|---|---|
| Document | Phase Implementation Plan |
| System | Modular Software Project Management System / MiniCoder-aligned platform concept |
| Status | Draft |
| Planning model | Foundation-first phased implementation |
| Explicit exclusions | No MVP; no premature end-to-end module before its substrate |
| Methodology authority | See SPMS-METHODOLOGY (reconciliation note) and SPMS-INDEX (register) |

---

# 1. Purpose

This document defines a phased implementation plan for the modular Software Project Management System using the previously defined module specifications and development requirements.

The plan deliberately avoids two common approaches:

- **No MVP**: the system must not begin as a simplified ticket tracker, document store, or isolated planning tool with governance, evidence, baselines, and traceability added later.
- **No premature end-to-end module**: the system must not drive one complete business module end-to-end to feature-completeness before the shared platform substrate it relies on is mature.

> **Terminology note (see `SPMS-METHODOLOGY`).** "Vertical slice" in the agile validation approach
> refers to *how each increment is built* (a thin slice through all layers) and is encouraged.
> The prohibition above is at the *macro sequencing* level only: foundation-first across phases,
> vertical slices within each phase. The two are complementary, not contradictory.

Instead, implementation proceeds through coherent architectural phases. Each phase produces a production-quality platform state with automated testing, deployment validation, evidence, observability, and clear exit criteria.

---

# 2. Implementation Principles

## 2.1 Foundation before modules

The following shared capabilities must be established before full functional modules are built on top of them:

- Identity, tenants, projects, products, and teams
- Common record model
- Metadata, classification, ownership, and lifecycle state
- Workflow, approval, gate, waiver, and delegation engine
- Traceability graph and relationship model
- Evidence repository and immutable audit log
- Baseline, version, and change-control engine
- Search, query, views, dashboards, and reporting framework
- Integration and event framework
- Object storage, relational database, graph projection, search index, and metrics store
- Administration, configuration, retention, backup, observability, and security

## 2.2 Every phase must be independently testable

Each phase must include:

- Implemented functionality
- Data model and migrations
- API layer
- UI/admin capability where needed
- Automated unit tests
- Automated integration tests
- Automated system tests
- Automated security checks
- Deployment automation
- Observability
- Documentation
- Acceptance criteria

## 2.3 Governance must not be bolted on later

Approvals, evidence, audit, baselines, waivers, change control, and historical reconstruction are core architectural capabilities. They must exist early enough that later modules reuse them rather than reimplementing them independently.

## 2.4 Testing and deployment automation are part of the product

The system must include tooling to manage development, test, staging, and production state without manual intervention. This includes:

- Database lifecycle management
- Test data lifecycle management
- Object storage test fixtures
- Trigger/workflow engine state reset and replay tooling
- Migration validation
- Seed data generation
- Environment reset tools
- Deployment smoke tests
- Rollback validation
- Backup and restore validation

---

# 3. Phase Overview

| Phase | Name | Main Outcome |
|---|---|---|
| 0 | Programme setup and architecture baseline | Delivery model, repository structure, standards, environments, CI/CD skeleton |
| 1 | Platform kernel | Tenant/project/team identity model, common records, permissions, admin shell |
| 2 | Lifecycle substrate | Workflow, approvals, gates, delegation, activity feed, audit events |
| 3 | Data substrate | Evidence store, object storage, baseline/version engine, historical reconstruction |
| 4 | Traceability substrate | Relationship graph, impact analysis, coverage rules, graph queries |
| 5 | Search, reporting, events, and automation substrate | Search, dashboards, event bus, rules engine, notifications |
| 6 | Planning, issues, and documents core | Work packages, issue/change management, controlled documents |
| 7 | Requirements and V&V core | Requirements, baselines, verification planning, test cases, test runs, evidence |
| 8 | Engineering pipeline integration | Git, CI/CD, build records, artifacts, automated test ingestion, provenance |
| 9 | Release, deployment, configuration, and assets | Releases, versions, environments, CIs, deployments, drift, rollback |
| 10 | Security, compliance, and product assurance | Vulnerabilities, controls, risks, waivers, NCRs, CAPA, assurance gates |
| 11 | Portfolio analytics and operational hardening | Cross-project dashboards, metrics, scale, resilience, backup, restore |
| 12 | AI assistance and advanced automation | Grounded AI, trace suggestions, evidence-gap detection, policy assistance |

---

# 4. Phase 0 — Programme Setup and Architecture Baseline

## Objective

Establish the engineering foundation before building product functionality.

## Scope

Implement the development operating model:

- Repository structure
- Backend module conventions
- Frontend module conventions
- Database migration framework
- API standards
- Test strategy
- CI/CD skeleton
- Local development environment
- Hosted development, test, and staging environments
- Coding standards
- Architecture decision record process
- Initial governance profile definitions

## Key Deliverables

- Architecture baseline document
- Module boundary map
- Domain model conventions
- API standards
- Testing standards
- CI/CD baseline
- Environment baseline
- Definition of done
- Release process for the platform itself

## Development Requirements

| Test Level | Required Automation |
|---|---|
| Unit | Domain models, validators, policies, utility libraries |
| Integration | Database, API, event bus, object storage, auth mocks |
| System | Start full system locally and exercise public APIs |
| Deployment | Build images, deploy to test environment, run smoke tests |
| Security | Dependency scan, secret scan, static analysis |
| Quality | Lint, type checks, formatting, architecture-boundary checks |

## Exit Criteria

- Developers can run the full platform locally.
- CI validates every pull request.
- Main branch is continuously deployable to a test environment.
- Database migrations are automated and reversible where practical.
- Architecture boundaries are enforced by tests or static rules.

---

# 5. Phase 1 — Platform Kernel

## Objective

Create the non-negotiable platform core that every module will depend on.

## Scope

Implement:

- Tenant / organization
- Portfolio / programme
- Product / system / service
- Project
- Team
- User
- Group
- Role
- Permission
- Governance profile
- Common record model
- Metadata model
- Classification model
- Lifecycle status field
- Ownership model
- Admin console shell

## Key Platform Capabilities

| Capability | Description |
|---|---|
| Tenant isolation | Logical isolation for organizations/customers |
| Project hierarchy | Tenant → portfolio → product/system → project |
| Team model | Team membership, roles, ownership |
| RBAC | Role-based permissions |
| ABAC-ready metadata | Classification, environment, customer, product, sensitivity |
| Common record identity | Stable IDs, created/updated metadata, owner, lifecycle status |
| Admin configuration | Basic tenant, project, user, role, and team administration |

## Development Requirements

- Unit tests for permission evaluation, role resolution, and metadata validation.
- Integration tests for tenant isolation and project-scoped access.
- API contract tests for all core APIs.
- System tests for user login, project creation, team assignment, and permissions.
- Migration tests for schema evolution.
- Security tests for cross-tenant access prevention.

## Exit Criteria

- A tenant can be created.
- Projects, products, teams, users, and roles can be managed.
- Permissions are enforced consistently through API and UI.
- All records use a common identity and metadata model.
- Cross-tenant and cross-project access is blocked by default.

---

# 6. Phase 2 — Lifecycle, Workflow, Approval, and Audit Substrate

## Objective

Implement the shared workflow and governance engine before any major module hardcodes its own lifecycle.

## Scope

Implement:

- Workflow definitions
- State models
- Transition rules
- Required-field validators
- Required-approval validators
- Approval requests
- Delegation
- Separation-of-duty rules
- Gate definitions
- Waiver/deviation workflow skeleton
- Activity feed
- Audit event log
- Notification hooks

## Key Capabilities

| Capability | Description |
|---|---|
| Configurable workflows | Different lifecycles per object type |
| Approval engine | Role-based approval, rejection, and rework |
| Gate engine | Baseline, architecture, security, test readiness, release readiness, acceptance |
| Waiver engine skeleton | Request, assess, approve, expire, renew |
| Delegation | Temporary approval delegation |
| Separation of duties | Prevent author/approver conflicts |
| Audit log | Who, what, when, why for controlled actions |
| Activity feed | Human-readable lifecycle history |

## Development Requirements

- Unit tests for workflow transition validation.
- Unit tests for approval and separation-of-duty rules.
- Integration tests for workflow persistence and audit generation.
- System tests for approval request, approval, rejection, and rework.
- Negative tests for invalid transitions.
- Audit integrity tests confirming no silent state mutation.

## Exit Criteria

- Any record type can be attached to a lifecycle.
- State transitions are policy-driven, not hardcoded.
- Approvals and rejections produce audit events.
- Delegation and separation of duties work.
- Gate decisions can be recorded with rationale.

---

---

# Milestone — Thin Governed Thread (between Phase 2 and Phase 3)

Before building the full data substrate and functional modules, carry one simple record type
end-to-end through the substrate as a single vertical slice: create → review → approve → attach
evidence → baseline → link → emit events → audit → reconstruct historical state, exposed through a
minimal UI and the public API.

This proves the substrate against real usage early, gives stakeholders a demonstrable governed
loop to fund against well before Phase 6, and surfaces integration defects in the hardest
components while they are cheap to fix. It is a vertical slice (how) that does not jump ahead of its
substrate (what) — consistent with SPMS-METHODOLOGY. Detail and rationale: SPMS-DELIVERY §3.

---

# 7. Phase 3 — Evidence, Object Storage, Baselines, Versioning, and Historical Reconstruction

## Objective

Make evidence, baselines, and historical reconstruction first-class services before controlled modules rely on them.

## Scope

Implement:

- Evidence registry
- Evidence metadata
- Object storage integration
- Attachment service
- Evidence integrity hash
- Evidence review status
- Record versioning
- Named baselines
- Baseline membership
- Baseline approval integration
- Baseline comparison
- Historical state reconstruction
- Retention policy skeleton

## Key Capabilities

| Capability | Description |
|---|---|
| Evidence item | File, log, report, scan, approval, test output, screenshot, SBOM |
| Evidence metadata | Source, owner, date, version, environment, build, approval state |
| Integrity | Hashes, immutable reference, provenance metadata |
| Versioned records | Preserve meaningful record changes |
| Named baselines | Freeze coherent sets of records |
| Baseline comparison | Added, removed, changed, unchanged |
| Historical reconstruction | State at date, baseline, release, deployment, acceptance |

## Development Requirements

- Unit tests for baseline membership and comparison.
- Integration tests for object storage, hash validation, and metadata.
- System tests for evidence upload, review, baseline creation, and baseline approval.
- Tamper-resistance tests for immutable evidence references.
- Backup/restore tests for object storage metadata and files.

## Exit Criteria

- Evidence can be uploaded, classified, linked, and reviewed.
- Baselines can be created, approved, locked, and compared.
- Historical record state can be reconstructed.
- Approved baselines cannot be silently altered.
- Evidence loss or tampering is detectable.

---

# 8. Phase 4 — Traceability Graph and Impact Analysis

## Objective

Implement the graph model that makes the platform an integrated lifecycle system rather than a collection of modules.

## Scope

Implement:

- Relationship type registry
- Link creation and deletion
- Link metadata
- Link provenance
- Required traceability rules
- Coverage rules
- Suspect link model
- Impact traversal
- Graph projection
- Graph query API
- Traceability matrix API
- Basic graph UI

## Required Initial Link Types

| Link Type | Example |
|---|---|
| derives-from | Requirement derives from stakeholder need |
| decomposes-to | Work package decomposes to task |
| implements | Build, work, or code implements requirement |
| verifies | Test verifies requirement |
| validates | Scenario validates stakeholder need |
| blocks | Task blocks release |
| depends-on | Service depends on API/database |
| deployed-to | Component deployed to environment |
| affects | Vulnerability affects asset |
| mitigates | Control mitigates risk |
| included-in | Requirement included in release |
| evidenced-by | Test result evidences verification |
| approved-by | Baseline approved by authority |

## Development Requirements

- Unit tests for relationship cardinality and validation rules.
- Integration tests for relational-to-graph projection.
- System tests for trace creation, navigation, and impact analysis.
- Performance tests for graph traversal on representative data volumes.
- Regression tests for suspect-link recalculation.
- Historical graph tests for baseline-time trace reconstruction.

## Exit Criteria

- Records can be linked bidirectionally.
- Impact analysis works across record types.
- Traceability matrices can be generated.
- Links can be marked suspect after upstream change.
- Coverage gaps can be detected.

---

# 9. Phase 5 — Search, Reporting, Events, Rules, and Notifications

## Objective

Add the common usability and automation substrate shared by all modules.

## Scope

Implement:

- Event bus
- Standard domain events
- Notification service
- Rule engine
- Policy-as-code framework
- Background job framework
- Full-text search
- Structured filters
- Saved views
- Dashboard framework
- Metrics model
- Report export skeleton
- Audit-safe automation actor model

## Key Capabilities

| Capability | Description |
|---|---|
| Event bus | RecordCreated, RecordUpdated, StateChanged, ApprovalCompleted, EvidenceAdded |
| Rules engine | Trigger-condition-action automation |
| Notifications | Email, in-app, webhook, digest |
| Search | Full-text and structured search |
| Saved views | Personal, team, project, audit, release views |
| Metrics | Flow, readiness, coverage, risk, quality |
| Reports | CSV, JSON, Markdown, PDF-ready exports |
| Automation identity | Bot actions are auditable and permission-scoped |

## Development Requirements

- Unit tests for rule evaluation.
- Integration tests for event publication and consumption.
- Search index consistency tests.
- System tests for notification delivery, saved views, and dashboard data.
- Load tests for search and dashboard queries.
- Security tests for automation actor permissions.

## Exit Criteria

- Modules can publish and consume standard events.
- Search works across common records.
- Dashboards can be configured from queryable metrics.
- Rules can automate common actions.
- Automated actions are fully auditable.

---

# 10. Phase 6 — Planning, Issue, Change, and Document Core

## Objective

Implement the first user-facing operational modules on top of the mature substrate.

This phase is not an MVP. It is the first coherent operational capability: planning, execution, issue/change handling, and controlled knowledge.

## Scope

Implement:

- Work package management
- WBS hierarchy
- Deliverable register
- Task/activity records
- Issue/change/defect records
- Backlog and queues
- Kanban-style boards
- Controlled documents
- Decision records
- Document review workflow
- Document versioning
- Links among work packages, tasks, issues, documents, decisions, and evidence

## Key Capabilities

| Module | Capabilities |
|---|---|
| Planning | Work packages, WBS, deliverables, dependencies, milestones |
| Issues | Bugs, tasks, actions, changes, incidents, defects, exceptions |
| Documents | Specs, plans, decisions, notes, runbooks, controlled docs |
| Collaboration | Comments, mentions, activity feeds, review assignments |
| Governance | Review, approval, baseline-ready records |
| Evidence | Attachments, closure evidence, decision evidence |
| Traceability | Work ↔ issues ↔ docs ↔ decisions ↔ evidence |

## Development Requirements

- Unit tests for WBS, issue lifecycle, and document lifecycle.
- Integration tests for workflows, approvals, evidence, and links.
- System tests for create-plan-execute-close flows.
- UI tests for board/list/detail/document views.
- Import/export tests for Markdown, CSV, and JSON.
- Accessibility tests for core UI flows.

## Exit Criteria

- Work packages can be planned, decomposed, tracked, and closed.
- Issues can be captured, triaged, assigned, resolved, and verified.
- Controlled documents can be drafted, reviewed, approved, versioned, and linked.
- Decisions are linked to work, issues, requirements-ready records, and evidence.
- Dashboards show work status, blockers, aging, and ownership.

---

# 11. Phase 7 — Requirements and Test/V&V Core

## Objective

Implement governed scope definition and verification capability.

## Scope

Implement:

- Requirement records
- Requirement sets
- Requirement hierarchy
- Requirement metadata
- Requirement review and approval
- Requirement baselines
- Requirement change control
- Verification method model
- Test case repository
- Test procedure records
- Test suite and campaign model
- Test execution records
- Manual result capture
- Automated result import API
- Verification evidence links
- Requirement-to-test coverage
- Acceptance package skeleton

## Key Capabilities

| Capability | Description |
|---|---|
| Requirements | Capture, author, structure, review, approve, baseline |
| Quality checks | Testability, completeness, ambiguity, duplicate detection |
| Traceability | Source/design/test/code/build/release/evidence links |
| Verification planning | Method, criteria, owner, evidence expectation |
| Test assets | Cases, procedures, suites, data, environments |
| Test execution | Manual and automated results |
| Coverage | Requirement, risk, regression, interface coverage |
| V&V evidence | Logs, reports, screenshots, test results |
| Acceptance | Evidence-based requirement acceptance |

## Development Requirements

- Unit tests for requirement validators and verification status logic.
- Integration tests for baselines, traceability, test execution, and evidence.
- System tests for requirement baseline → test planning → execution → verification approval.
- Automated import tests for JUnit/xUnit/pytest-style result formats.
- Coverage calculation tests.
- Mutation/regression tests for requirement change impact.

## Exit Criteria

- Requirements can be baselined and changed under control.
- Requirements can be linked to verification methods and test cases.
- Test runs can produce evidence.
- Automated test results can be imported.
- Requirement verification status is calculated from controlled evidence.
- Coverage gaps are visible.

---

# 12. Phase 8 — Engineering Pipeline, Git, Build, Artifact, and Provenance Integration

## Objective

Connect the system to real software engineering execution.

## Scope

Implement:

- Git provider integration
- Repository registry
- Branch/commit/PR records
- Pipeline definition references
- Pipeline run records
- Build records
- Job/stage/step records
- Artifact records
- Artifact metadata
- Artifact checksum/signature fields
- Build-to-test result links
- Build-to-requirement links
- CI status ingestion
- Pipeline evidence capture
- Provenance model
- Basic artifact repository integration

## Key Capabilities

| Capability | Description |
|---|---|
| Git integration | Repos, branches, commits, PRs, tags |
| Pipeline ingestion | Runs, stages, jobs, logs, status |
| Build records | Commit, branch, toolchain, runner, result |
| Artifact records | Package/image/binary metadata, checksum, signature |
| Test result ingestion | Link automated results to builds and requirements |
| Provenance | Source, build process, dependency, runner, artifact |
| Gates | Quality/security/release readiness inputs |
| Evidence | Logs, reports, scans, SBOMs, attestations |

## Development Requirements

- Unit tests for provenance and artifact metadata validation.
- Integration tests with mocked Git and CI systems.
- Contract tests for webhook payloads.
- System tests for commit → build → test result → evidence → requirement trace.
- Security tests for webhook authenticity and secret masking.
- Performance tests for large pipeline log ingestion.

## Exit Criteria

- Commits, PRs, builds, tests, artifacts, and evidence are linked.
- Build provenance is queryable.
- Automated test results update V&V records.
- Pipeline failures can create issues.
- Artifacts can be promoted only through defined gates.

---

# 13. Phase 9 — Release, Deployment, Configuration, Environment, and Asset Management

## Objective

Add controlled delivery and operational-state management.

## Scope

Implement:

- Release records
- Version registry
- Release scope
- Release baseline
- Release readiness checklist
- Release approval workflow
- Deployment plan
- Deployment run
- Deployment step records
- Environment registry
- Configuration item registry
- Asset registry
- Deployment inventory
- Environment topology
- Configuration baseline
- Drift detection skeleton
- Rollback plan records
- Operational handover package

## Key Capabilities

| Capability | Description |
|---|---|
| Release planning | Scope, target date, owner, release type |
| Version registry | Product/component/API/schema/config/document versions |
| Release baseline | Requirements, issues, builds, artifacts, tests, docs, approvals |
| Readiness | Requirements, issues, tests, security, docs, operations |
| Deployment | Plan, window, topology, strategy, steps, approval, logs |
| Rollback | Rollback criteria, previous versions, verification |
| Environments | Dev/test/staging/prod/DR/customer/lab |
| CIs/assets | Applications, services, databases, infra, documents, tools |
| Drift | Expected vs actual environment/config state |
| Handover | Runbooks, monitoring, support, access, evidence |

## Development Requirements

- Unit tests for release state model, readiness calculation, and deployment status.
- Integration tests for release baseline, artifact links, and deployment logs.
- System tests for release creation → readiness → approval → deployment → verification → closure.
- Deployment smoke tests in real test/staging environments.
- Rollback simulation tests.
- Drift detection tests using declared vs observed configuration fixtures.

## Exit Criteria

- A release can be scoped, baselined, approved, deployed, verified, and closed.
- Deployed versions are visible by environment.
- Deployment logs and post-deployment verification are evidence.
- Environment and CI records support impact analysis.
- Rollback readiness is checked before deployment.

---

# 14. Phase 10 — Security, Compliance, Product Assurance, NCR, Waiver, and CAPA

## Objective

Implement the cross-cutting assurance system that governs security, compliance, product quality, deviations, and corrective actions.

## Scope

Implement:

- Security control library
- Compliance mapping
- Security requirement links
- Vulnerability records
- Vulnerability intake API
- Vulnerability triage workflow
- Risk register
- Threat model records
- Exception/waiver records
- Waiver expiry and renewal
- NCR records
- CAPA records
- Assurance plan
- Assurance tailoring model
- Quality gate checklists
- Audit finding records
- Security release gate
- Compliance evidence package

## Key Capabilities

| Capability | Description |
|---|---|
| Controls | Control library, applicability, ownership, evidence |
| Vulnerabilities | Intake, classification, prioritization, assignment, remediation, verification |
| Risk | Risk register, treatment, acceptance, review cadence |
| Threat models | Data flows, threats, mitigations, coverage |
| Waivers | Rationale, risk, compensating controls, expiry, approval |
| NCRs | Nonconformance workflow, disposition, evidence, closure |
| CAPA | Corrective/preventive actions, effectiveness verification |
| PA gates | Baseline, design, test, release, deployment, acceptance |
| Compliance | Mapping to standards, controls, evidence, audit findings |
| Security gates | Vulnerability thresholds, SBOM, signing, threat model, privacy |

## Development Requirements

- Unit tests for vulnerability prioritization and SLA rules.
- Unit tests for waiver expiry and renewal rules.
- Integration tests for vulnerabilities linked to assets, builds, releases, and issues.
- System tests for finding → remediation issue → build → verification → closure.
- System tests for NCR → CAPA → effectiveness verification.
- Security gate tests with pass/fail/waived cases.
- Audit package generation tests.

## Exit Criteria

- Vulnerabilities can be imported, triaged, assigned, fixed, verified, waived, or closed.
- Security controls can be mapped to evidence.
- Waivers and NCRs are controlled records with expiry, approval, and evidence.
- CAPA actions can be verified for effectiveness.
- Release gates can block on security, evidence, NCR, waiver, or compliance conditions.
- Product acceptance can include controlled residual risk.

---

# 15. Phase 11 — Portfolio Analytics, Operational Hardening, Scale, Backup, and Restore

## Objective

Make the system robust for real multi-project, multi-team, long-running operation.

## Scope

Implement:

- Portfolio dashboards
- Executive reporting
- Cross-project dependencies
- Cross-product release views
- Evidence completeness dashboards
- Risk heatmaps
- Quality trends
- Security posture dashboards
- Environment drift dashboards
- Performance optimization
- Data partitioning strategy
- Backup and restore automation
- Disaster recovery runbooks
- Retention and archival policies
- Observability dashboards
- Admin health console

## Key Capabilities

| Capability | Description |
|---|---|
| Portfolio reporting | Progress, risks, dependencies, readiness, releases |
| Cross-project analytics | Flow, capacity, blockers, quality, traceability |
| Evidence reporting | Missing, stale, rejected, expired evidence |
| Security reporting | Vulnerability aging, exceptions, controls, posture |
| Operational reporting | Deployments, incidents, drift, environment health |
| Reliability | Backup, restore, DR, monitoring, alerting |
| Scale | Large records, large graphs, large evidence stores |
| Administration | Tenant health, jobs, integrations, queues, storage |

## Development Requirements

- Load tests with representative multi-project data.
- Graph traversal performance tests.
- Search indexing performance tests.
- Backup/restore tests with relational DB, object store, search, and graph projection.
- Chaos/failure tests for workers, queues, event bus, and storage.
- Security tests for data retention, archival, and tenant boundaries.
- Observability acceptance tests.

## Exit Criteria

- The system supports multiple products, projects, teams, releases, and environments.
- Backup and restore are proven.
- Dashboards remain performant at expected scale.
- Evidence and audit records remain reconstructable.
- Operations team has monitoring and runbooks.

---

# 16. Phase 12 — AI Assistance and Advanced Automation

## Objective

Add AI as a governed assistant, not as an authority.

AI should help draft, classify, summarize, suggest trace links, detect evidence gaps, answer with citations, and assist impact analysis. It must not silently approve, baseline, release, waive, or accept controlled records.

## Scope

Implement:

- Governed retrieval over approved records
- Source-grounded Q&A
- Summarization
- Draft generation
- Classification suggestions
- Duplicate detection
- Traceability suggestions
- Impact analysis assistance
- Evidence gap detection
- Release note drafting
- Test suggestion
- Requirement quality suggestions
- Security remediation suggestions
- Human approval workflow for AI-generated changes
- AI audit trail

## Key Capabilities

| Capability | Description |
|---|---|
| Grounded Q&A | Answers cite source records/evidence |
| Drafting | Requirements, issues, release notes, reports, test cases |
| Classification | Type, owner, severity, priority, control, component |
| Trace suggestions | Candidate links with confidence and rationale |
| Impact assistance | Summarize affected records and suspected gaps |
| Evidence gaps | Missing/stale/weak evidence detection |
| Review assistance | Summarize unresolved comments, weak claims, missing sections |
| Human approval | AI suggestions require human acceptance |
| Auditability | AI prompt, sources, output, accepted/rejected state |

## Development Requirements

- Evaluation datasets for AI retrieval quality.
- Tests for citation grounding.
- Tests for permission-scoped retrieval.
- Unsupported-claim detection checks.
- Red-team tests for data leakage across tenants/projects.
- Human-in-the-loop workflow tests.
- Regression tests for AI-generated structured output.

## Exit Criteria

- AI answers are source-grounded and permission-scoped.
- AI suggestions never bypass approval workflows.
- AI-generated changes are auditable.
- Evidence-gap and traceability suggestions improve coverage without silently changing controlled records.

---

# 17. Cross-Phase Automated Testing Strategy

## 17.1 Required Test Pyramid

| Level | Purpose | Examples |
|---|---|---|
| Unit tests | Fast validation of domain rules | Permissions, workflow transitions, baseline diff, readiness calculation |
| Component tests | Module boundary validation | Requirements API, issue API, evidence service, graph service |
| Integration tests | Real infrastructure interactions | DB, object storage, event bus, search, graph projection |
| Contract tests | API and webhook stability | Git, CI/CD, scanner, test result import payloads |
| System tests | End-to-end platform behavior | Baseline → test → release → deployment → acceptance |
| Deployment tests | Verify deployability | Migrations, smoke tests, rollback, health checks |
| Security tests | Protect system and data | RBAC/ABAC, tenant isolation, secret scans, dependency scans |
| Performance tests | Scale confidence | Graph traversal, dashboard queries, search, evidence upload |
| Resilience tests | Operational confidence | Backup/restore, worker failure, queue retry, object-store outage |

## 17.2 Quality Gates Per Pull Request

Every pull request should require:

- Build passes
- Unit tests pass
- Integration tests for affected modules pass
- API contract tests pass
- Lint/type/static checks pass
- Architecture-boundary checks pass
- Security dependency scan pass or approved exception
- Secret scan pass
- Migration validation pass
- Documentation updated where needed

## 17.3 Quality Gates Per Release Candidate

Every release candidate should require:

- Full system test suite
- Regression suite
- Database migration test
- Deployment smoke test
- Rollback/recovery test where applicable
- Evidence completeness check
- Security scan
- SBOM generation
- Release notes generation
- Operational readiness check
- Approval by release authority

---

# 18. Development and Production State Management Requirements

The system must provide built-in tooling for deterministic state management across local development, CI, test, staging, and production.

## 18.1 Database lifecycle tooling

Required capabilities:

- Create database
- Migrate database
- Roll back migration where supported
- Validate migration history
- Reset development database
- Seed deterministic test data
- Create anonymized test fixtures
- Snapshot and restore test database
- Verify backup integrity
- Run migration dry-run in CI

## 18.2 Workflow engine state tooling

Required capabilities:

- Reset workflow state in development/test
- Replay workflow events
- Inspect stuck workflow runs
- Cancel test workflow runs
- Requeue failed jobs
- Drain queues before deployment
- Export workflow execution evidence
- Validate scheduled job configuration

## 18.3 Object storage lifecycle tooling

Required capabilities:

- Create development/test buckets
- Seed test evidence objects
- Validate object metadata
- Verify evidence hashes
- Garbage-collect orphaned test objects
- Snapshot and restore evidence store metadata
- Test object retention rules

## 18.4 Search and graph projection tooling

Required capabilities:

- Rebuild search index
- Rebuild graph projection
- Validate projection consistency
- Compare relational state to graph state
- Recalculate coverage metrics
- Recalculate suspect links
- Validate dashboard aggregates

## 18.5 Production-safe operational tooling

Required capabilities:

- Backup before migration
- Verify backup after migration
- Run smoke tests after deployment
- Run rollback simulation where possible
- Validate background workers are healthy
- Validate queues are processing
- Validate event consumers are current
- Validate scheduled jobs are registered
- Export deployment evidence package

---

# 19. Recommended Build Order Summary

The recommended build order is:

1. Build the platform kernel first.
2. Build workflow, evidence, audit, baseline, and traceability before major modules.
3. Build planning/issues/documents as the first operational capability.
4. Add requirements and V&V once traceability and baselines are ready.
5. Add CI/CD integration once requirements/tests/evidence can consume results.
6. Add release/deployment once builds, artifacts, tests, environments, and approvals exist.
7. Add security/product assurance once evidence, release gates, vulnerabilities, NCRs, waivers, and assets can be connected.
8. Add analytics, scale, and AI after the governed data fabric is mature.

This sequence keeps the system coherent and avoids the common failure mode of building disconnected modules that later require expensive rework to add traceability, evidence, baselines, and governance.

---

# 20. Final Acceptance Criteria for the Implementation Programme

The implementation programme is complete when the system can demonstrate the following end-to-end capabilities across multiple projects and teams:

1. A requirement can be captured, reviewed, approved, baselined, changed under control, implemented, verified, and accepted.
2. A work package can be planned, decomposed, executed, linked to deliverables, and closed with evidence.
3. An issue or change can be raised, triaged, assigned, implemented, verified, linked to release scope, and closed.
4. A document can be drafted, reviewed, approved, versioned, baselined, and linked to requirements, decisions, tests, releases, and evidence.
5. Automated CI/CD results can be ingested and linked to code, builds, artifacts, tests, requirements, and releases.
6. A release can be scoped, baselined, approved, deployed, verified, and closed with full evidence.
7. Environments, assets, configuration items, and deployed versions can be queried and used for impact analysis.
8. Vulnerabilities, controls, risks, waivers, NCRs, and CAPA actions can be governed and linked to affected records.
9. Product assurance can determine whether a release or product is ready for acceptance.
10. Historical state can be reconstructed for a baseline, release, deployment, audit period, or acceptance decision.
11. The full system can be tested, deployed, backed up, restored, and operated without manual intervention.
12. AI assistance can support drafting, summarization, classification, traceability, and evidence-gap detection without bypassing governance.
