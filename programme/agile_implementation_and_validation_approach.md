# Agile Implementation and Validation Approach

## Modular Software Project Management System

| Field | Value |
|---|---|
| Document type | Development and validation standard |
| Scope | Implementation, testing, release, deployment, and operational validation of the modular Software Project Management System |
| Intended users | Engineering leads, architects, developers, QA/test engineers, DevOps engineers, product owners, security reviewers, release managers |
| Status | Draft |
| Orientation | Agile, automation-first, risk-based, low-friction governance |

---

# 1. Purpose

This document defines an agile implementation and validation approach for building the modular Software Project Management System.

It does **not** define what the system must do for its end users. Instead, it defines **how the system should be implemented, tested, validated, integrated, released, and operated**.

The aim is to achieve high engineering confidence through automation while avoiding a heavy audit-driven development process.

The approach is based on four principles:

1. **Working software is the primary proof of progress.**
2. **Automated validation is preferred over manual review and evidence collection.**
3. **Governance is applied according to risk, not uniformly to every change.**
4. **Production safety, security, tenant isolation, data integrity, and reversibility remain strict.**

---

# 2. Scope

## 2.1 Included

This approach applies to the implementation of:

- platform core;
- shared substrate services;
- functional modules;
- APIs;
- UI applications;
- workflow engines;
- traceability graph;
- evidence and audit services;
- CI/CD integrations;
- release and deployment capabilities;
- configuration and environment management;
- security and compliance capabilities;
- AI-assisted functions;
- reporting and analytics;
- operational monitoring and support functions.

## 2.2 Excluded

This document does not define:

- detailed user-facing functional requirements;
- detailed UX specifications;
- database schema design;
- individual module specifications;
- compliance certification procedures;
- formal product assurance process for regulated delivery;
- customer acceptance process for contractual delivery.

Those may exist separately where required.

---

# 3. Overall Agile Delivery Model

The system should be delivered as a sequence of coherent, production-quality increments.

Each increment should:

- deliver usable software;
- preserve architectural integrity;
- include automated validation;
- be deployable to a real environment;
- improve or extend an end-to-end capability;
- leave the system in a known, observable, recoverable state.

The preferred delivery pattern is **vertical slicing**.

> **Scope note (see `SPMS-METHODOLOGY`).** Vertical slicing here governs *how each increment is
> built* — a thin slice through all layers rather than all-backend-then-all-UI. It operates inside
> the foundation-first phase sequence of the Phase Implementation Plan, which governs *what is built
> before what*. The Phase Plan's "no premature end-to-end module" rule and this vertical-slicing
> preference are complementary: foundation-first across phases, vertical slices within each phase.

A vertical slice should include enough of the following to prove the feature works end to end:

- domain model;
- API;
- persistence;
- permissions;
- workflow behaviour;
- UI where relevant;
- events or integration behaviour;
- automated tests;
- deployment configuration;
- observability;
- documentation or release note where needed.

Avoid building all backend first, then all UI, then all integrations. That delays validation and increases integration risk.

---

# 4. Engineering Philosophy

## 4.1 Automation over paperwork

The system should produce confidence through:

- automated tests;
- CI/CD gates;
- preview environments;
- deployment smoke tests;
- synthetic checks;
- monitoring;
- contract tests;
- security scans;
- migration tests;
- rollback tests;
- code review.

Formal evidence packs should not be required for ordinary development work.

## 4.2 Review where it matters

Manual approval should be reserved for:

- production deployment;
- security-sensitive changes;
- permissions and tenant isolation;
- irreversible data migration;
- major architectural decisions;
- high-risk release decisions;
- accepted security risk;
- customer-facing contractual acceptance;
- changes to core governance behaviour.

Normal feature development should not require formal approval beyond peer review and automated checks.

## 4.3 Traceability should be useful, not exhaustive

Every change should be linked to a work item, but the system should not require a full traceability matrix for every small change.

Useful traceability includes:

- issue/story to pull request;
- pull request to build;
- build to artifact;
- artifact to deployment;
- test result to build;
- release to included issues;
- production deployment to release version.

Detailed requirement-to-test-to-evidence traceability should be reserved for controlled or high-risk features.

## 4.4 Risk-based rigor

Not all changes deserve the same process.

A typo fix, dashboard improvement, or low-risk UI enhancement should not follow the same process as an authorization change, tenant-isolation change, database migration, or production deployment change.

The implementation process should therefore use governance levels.

---

# 5. Governance Levels

## 5.1 Level 1 — Lightweight Change

Use for ordinary agile delivery.

Typical examples:

- UI refinements;
- dashboard/report improvements;
- minor workflow usability changes;
- low-risk bug fixes;
- documentation updates;
- internal refactoring with no behaviour change;
- minor API additions that do not break compatibility;
- non-sensitive configuration improvements.

Required:

- issue, story, or task exists;
- acceptance criteria are clear enough to test;
- code review by at least one peer;
- relevant unit tests pass;
- relevant integration or UI tests pass where behaviour changes;
- CI pipeline passes;
- no critical security finding is introduced;
- deployment to development, test, or preview environment succeeds where applicable;
- smoke test passes where applicable.

Not required:

- formal approval workflow;
- explicit evidence package;
- manual release board;
- full traceability matrix;
- electronic signature;
- formal baseline;
- formal waiver for minor non-blocking limitations.

## 5.2 Level 2 — Controlled Change

Use for changes with architectural, integration, data, workflow, or cross-module impact.

Typical examples:

- public API changes;
- event schema changes;
- workflow engine changes;
- search indexing changes;
- graph projection changes;
- baseline/versioning changes;
- release or deployment logic changes;
- integration with CI/CD, Git, scanner, identity, or monitoring tools;
- database schema migration;
- import/export format changes;
- permission model extension;
- configuration model changes.

Required:

- linked issue, story, change, or work package;
- acceptance criteria;
- short design note or ADR if architecture changes;
- peer review by relevant owner;
- unit tests;
- integration tests;
- contract tests if APIs/events/imports/exports change;
- migration tests if persistence changes;
- targeted end-to-end test;
- security review where security behaviour changes;
- release note if user-visible or operator-visible;
- deployment smoke test.

Optional:

- lightweight risk note;
- rollback note;
- test summary;
- operations note.

## 5.3 Level 3 — High-Risk Change

Use for changes where failure can compromise production safety, data integrity, security, or trust.

Typical examples:

- authentication;
- authorization;
- tenant isolation;
- audit log integrity;
- evidence integrity;
- secret handling;
- production deployment automation;
- destructive or irreversible migration;
- data deletion and retention;
- backup and restore;
- artifact signing and provenance;
- vulnerability gating;
- high-risk AI-assisted automation;
- changes to production approval rules;
- changes to separation-of-duty enforcement;
- changes affecting customer data or regulated data.

Required:

- linked controlled change record;
- clear acceptance and rollback criteria;
- design/decision note;
- two-person review;
- security review where relevant;
- unit tests;
- integration tests;
- contract tests;
- system/end-to-end tests;
- migration and rollback validation;
- staging deployment;
- production deployment approval;
- smoke/synthetic checks;
- monitoring verification after deployment;
- explicit release note or operational communication;
- follow-up action for any accepted residual risk.

---

# 6. Definition of Ready

A story or change is ready for implementation when:

- the intended outcome is understandable;
- acceptance criteria exist;
- dependencies are identified;
- risk level is assigned;
- impacted modules or services are roughly known;
- test approach is understood;
- required data, environment, or integration dependency is available or planned;
- unresolved open questions are small enough not to block development.

For Level 2 and Level 3 changes, readiness should also include:

- architecture impact considered;
- migration impact considered;
- security impact considered;
- deployment and rollback implications considered.

---

# 7. Definition of Done

## 7.1 Standard Definition of Done

A change is done when:

- acceptance criteria are satisfied;
- code has been reviewed;
- CI pipeline passes;
- relevant automated tests pass;
- no critical or high-severity blocker remains;
- user-visible behaviour is documented where needed;
- operationally relevant behaviour is observable where needed;
- deployment to the intended non-production environment succeeds where applicable.

## 7.2 Additional Done Criteria for Controlled Changes

For Level 2 changes, also require:

- contract tests updated where interfaces changed;
- migration tests completed where data changed;
- relevant end-to-end test added or updated;
- release notes updated where needed;
- monitoring/logging updated where behaviour requires operational visibility;
- backwards compatibility decision documented.

## 7.3 Additional Done Criteria for High-Risk Changes

For Level 3 changes, also require:

- rollback or forward-fix path validated;
- staging deployment completed;
- security-sensitive behaviour reviewed;
- production monitoring and alerting checked;
- deployment approval obtained;
- post-deployment smoke or synthetic tests pass;
- residual risk explicitly accepted where applicable.

---

# 8. Source Control and Branching

## 8.1 Repository Rules

All implementation assets should be version controlled, including:

- application source code;
- database migrations;
- infrastructure definitions;
- test code;
- pipeline definitions;
- policy-as-code rules;
- API schemas;
- event schemas;
- configuration templates;
- documentation close to code.

## 8.2 Branching Model

Recommended model:

- `main` is always releasable;
- feature branches are short-lived;
- release branches are used only when necessary;
- hotfix branches are allowed for urgent production fixes;
- tags identify release candidates and released versions.

## 8.3 Pull Request Rules

Every non-trivial change should use a pull request.

A pull request should show:

- linked issue/story/change;
- scope of change;
- tests run;
- risks or migration notes if relevant;
- screenshots or recordings for significant UI changes;
- API/schema notes where relevant;
- reviewer approval.

The merge gate should be automated wherever possible.

---

# 9. CI/CD Pipeline Model

## 9.1 Pull Request Pipeline

Run on every pull request:

- format check;
- linting;
- type checking;
- unit tests;
- affected integration tests;
- API/event contract tests when relevant files changed;
- architecture boundary checks;
- dependency vulnerability scan;
- secret scan;
- build;
- basic package/container validation.

Blocking failures:

- failed build;
- failed unit tests;
- failed affected integration tests;
- failed contract tests for changed APIs/events;
- critical vulnerability introduced;
- secret detected;
- architecture boundary violation;
- migration validation failure;
- permission/tenant isolation regression.

Warnings:

- minor coverage drop;
- low-severity vulnerability;
- flaky test warning;
- non-critical documentation gap;
- performance warning outside release threshold.

## 9.2 Main Branch Pipeline

Run after merge:

- full unit suite;
- full integration suite;
- core end-to-end suite;
- full build/package/container creation;
- artifact metadata generation;
- SBOM generation;
- artifact scan;
- artifact publishing to non-production repository;
- deployment to shared integration environment or preview environment;
- smoke tests.

## 9.3 Nightly Pipeline

Run slower checks outside the PR path:

- full end-to-end regression;
- full search/graph projection rebuild test;
- larger migration rehearsal;
- backup/restore smoke test;
- dependency update check;
- accessibility tests;
- performance smoke tests;
- security scan expansion;
- flaky test detection;
- long-running integration checks;
- data import/export regression tests.

## 9.4 Release Candidate Pipeline

Run before release candidate approval:

- full regression suite;
- full security scan set;
- migration validation;
- rollback rehearsal for risky changes;
- deployment to staging;
- staging smoke tests;
- synthetic transaction checks;
- release notes generation;
- artifact signing;
- provenance/attestation generation where used;
- operational readiness check;
- release readiness summary.

## 9.5 Production Deployment Pipeline

Run for production deployment:

- confirm approved release candidate;
- confirm artifact identity and immutability;
- validate target environment health;
- validate configuration;
- validate secret references;
- confirm backup where required;
- deploy;
- run smoke tests;
- run synthetic checks;
- verify monitoring;
- support rollback or forward-fix;
- publish deployment result.

---

# 10. Testing Strategy

## 10.1 Test Pyramid

The preferred automated test distribution is:

| Level | Purpose | Expected volume |
|---|---|---|
| Unit tests | Fast validation of domain logic and rules | High |
| Component tests | Validate module behaviour with controlled dependencies | Medium-high |
| Integration tests | Validate real service/database/search/graph/event behaviour | Medium |
| Contract tests | Protect APIs, events, imports, and exports | Medium |
| End-to-end tests | Validate critical user and system journeys | Low-medium |
| Deployment tests | Validate installation, migration, smoke, rollback | Targeted |
| Performance/security/resilience tests | Validate non-functional risk areas | Targeted and scheduled |

The pyramid should avoid excessive fragile UI-only testing.

## 10.2 Unit Testing Requirements

Unit tests should cover:

- domain validation;
- lifecycle transition rules;
- workflow guard conditions;
- permission decisions;
- policy evaluation;
- traceability link validation;
- search query parsing;
- import/export transformations;
- baseline comparison;
- waiver expiry logic;
- date and SLA calculations;
- risk and severity scoring;
- event payload generation;
- audit event generation where applicable.

Do not require unit tests for:

- trivial DTOs;
- simple getters/setters;
- boilerplate mapping with no logic;
- visual-only components already covered elsewhere.

## 10.3 Integration Testing Requirements

Integration tests should cover:

- API and database persistence;
- transaction boundaries;
- optimistic locking;
- search indexing;
- graph projection;
- object storage references;
- event publishing and consumption;
- workflow engine integration;
- identity and permissions integration;
- CI/CD result import;
- scanner result import;
- release/deployment record creation;
- configuration drift ingestion;
- audit event creation.

## 10.4 Contract Testing Requirements

Contract tests are required for:

- public APIs;
- internal module APIs used by multiple modules;
- event schemas;
- webhook payloads;
- import/export formats;
- plugin interfaces;
- scanner integrations;
- CI/CD integrations;
- identity provider integration assumptions;
- AI-assistance API boundaries.

Contract tests should verify:

- schema compatibility;
- required fields;
- error formats;
- pagination/filtering behaviour;
- authentication and authorization expectations;
- backward compatibility;
- idempotency where applicable.

## 10.5 End-to-End Testing Requirements

End-to-end tests should focus on critical journeys.

Recommended core journeys:

1. Create issue → implement fix → close issue.
2. Create requirement → link test → verify requirement.
3. Create document → review → publish.
4. Create test run → import automated result → update verification status.
5. Create release → attach build → deploy to staging.
6. Create vulnerability → triage → remediate → verify.
7. Detect environment drift → create remediation → resolve.
8. Permission denial for unauthorized action.
9. Tenant A cannot access Tenant B data.
10. Create release candidate → run readiness checks → deploy → smoke test.

Avoid creating E2E tests for every UI variation. Prefer lower-level tests for edge cases.

## 10.6 Regression Testing

Regression testing should be change-based.

The system should select tests based on:

- changed files;
- changed modules;
- changed APIs;
- changed requirements;
- changed workflows;
- changed permissions;
- changed database schemas;
- changed infrastructure or deployment configuration;
- previous failures;
- risk profile.

Full regression should run before release and periodically overnight.

---

# 11. Security Validation

Security validation should be continuous and automated.

Required checks:

- dependency vulnerability scanning;
- container scanning where containers are used;
- static application security testing;
- infrastructure-as-code scanning;
- secret scanning;
- license checks;
- authentication tests;
- authorization tests;
- tenant-isolation tests;
- role and permission regression tests;
- audit-log integrity tests for sensitive actions;
- security header/configuration checks where applicable;
- artifact signing or provenance checks where applicable.

For ordinary low-risk changes, security validation should be mostly automated.

Manual security review is required for:

- authentication changes;
- authorization changes;
- tenant boundary changes;
- secret handling;
- encryption changes;
- externally exposed API changes;
- audit/evidence integrity changes;
- production deployment permission changes;
- high-risk AI automation.

---

# 12. Data, Migration, and Persistence Validation

Data correctness is a high-risk area.

Required validation for schema or data changes:

- migration applies cleanly to an empty database;
- migration applies cleanly to representative existing data;
- migration is repeat-safe where applicable;
- rollback or forward-fix strategy exists;
- data integrity constraints hold after migration;
- indexes and query plans are acceptable for expected scale;
- search and graph projections remain rebuildable;
- tenant boundaries remain intact;
- audit-relevant history is preserved.

For high-risk migrations:

- run migration rehearsal in staging;
- take backup before production;
- verify restore procedure where appropriate;
- run post-migration validation queries;
- monitor application errors after deployment.

---

# 13. Deployment Validation

Deployment validation should be automated.

Minimum deployment checks:

- target environment exists and is reachable;
- configuration is valid;
- required secrets are available through approved references;
- database migration state is known;
- dependent services are reachable or intentionally mocked;
- service starts successfully;
- health check passes;
- readiness check passes;
- smoke test passes;
- deployment result is recorded;
- monitoring receives expected signals.

For production:

- deployment uses an approved artifact;
- deployment happens through the pipeline;
- manual production changes are discouraged;
- rollback or forward-fix path is known;
- deployment is observable;
- critical alerts are active;
- post-deployment validation runs automatically.

---

# 14. Environment Strategy

## 14.1 Required Environments

Recommended minimum environments:

| Environment | Purpose |
|---|---|
| Local | Fast developer feedback |
| CI ephemeral | Isolated automated testing |
| Development/shared integration | Early cross-module integration |
| Preview | Per-branch or per-PR validation where feasible |
| Staging | Production-like release validation |
| Production | Live service |

Optional:

- performance environment;
- security test environment;
- migration rehearsal environment;
- demo environment;
- customer-specific sandbox.

## 14.2 Environment Rules

Each environment should have:

- clear owner;
- purpose;
- access rules;
- deployment method;
- data policy;
- reset or refresh approach;
- monitoring level;
- allowed test types;
- configuration source;
- secret source;
- drift detection approach.

Production and staging should not be manually modified except through controlled emergency procedures.

---

# 15. Observability and Operational Readiness

Every production-capable service should provide:

- health endpoint;
- readiness endpoint;
- structured logs;
- metrics;
- tracing where useful;
- error reporting;
- audit events for sensitive actions;
- dashboards for core service health;
- alerts for critical failure modes.

Operational readiness should be required before production release.

Minimum operational readiness checklist:

- service health visible;
- deployment status visible;
- error rate visible;
- latency visible;
- resource usage visible;
- critical background jobs visible;
- failed integration events visible;
- backup status visible where applicable;
- rollback or recovery procedure known.

---

# 16. Release Model

## 16.1 Normal Release

A normal release requires:

- main branch green;
- release candidate built from known commit;
- release notes generated or updated;
- staging deployment successful;
- smoke tests pass;
- no unresolved critical defect;
- no unresolved critical/high security issue unless explicitly accepted;
- production deployment approved by release owner.

## 16.2 Hotfix Release

A hotfix release requires:

- linked incident or defect;
- minimal targeted fix;
- targeted regression test;
- build and security checks;
- staging or equivalent validation if time allows;
- production approval;
- post-deployment monitoring;
- follow-up cleanup issue if process or test debt remains.

## 16.3 Major Release

A major release requires:

- full regression;
- migration rehearsal where applicable;
- rollback/forward-fix plan;
- operational readiness review;
- security scan review;
- documentation update;
- stakeholder review where appropriate;
- production deployment plan.

---

# 17. Evidence Model: Lightweight by Default

The system should not require formal evidence packages for normal agile work.

Instead, use automatic evidence produced by tools.

| Evidence | Source |
|---|---|
| Code review | Pull request |
| Test results | CI system |
| Build result | Pipeline run |
| Artifact identity | Artifact repository |
| Deployment status | Deployment pipeline |
| Security scan | Scanner output |
| Issue linkage | Issue tracker / Git integration |
| Release contents | Release record or Git tag |
| Logs and metrics | Observability platform |
| Smoke test result | Deployment pipeline |

Explicit evidence records are required only for:

- production release approval;
- high-risk security changes;
- tenant isolation changes;
- major data migration;
- destructive operations;
- customer acceptance;
- compliance-sensitive release;
- formal risk acceptance;
- major incident follow-up.

---

# 18. Documentation Approach

Documentation should be lightweight and close to the work.

Required documentation types:

| Document type | When required |
|---|---|
| README | For each service, module, or package |
| API documentation | For public or cross-module APIs |
| ADR | For material architectural decisions |
| Migration note | For significant schema or data changes |
| Release note | For user-visible or operator-visible changes |
| Runbook | For production services and operational procedures |
| Security note | For security-sensitive design choices |
| Test note | For unusual or high-risk validation approaches |

Avoid large documents that are not maintained.

Prefer:

- docs-as-code;
- generated API docs;
- short ADRs;
- living runbooks;
- examples close to code;
- diagrams where they clarify architecture.

---

# 19. AI-Assisted Development and Validation

AI assistance may be used to improve speed and quality, but should not bypass engineering controls.

Allowed uses:

- draft test cases;
- suggest edge cases;
- summarize failed logs;
- propose documentation updates;
- draft release notes;
- suggest trace links;
- analyze likely impact;
- identify missing tests;
- suggest refactoring;
- explain unfamiliar code.

Rules:

- AI-generated code must be reviewed like human-written code;
- AI-generated tests must be executed and reviewed;
- AI-generated documentation must be checked for accuracy;
- AI must not approve changes;
- AI must not override security gates;
- AI must not mark requirements, tests, releases, or deployments as accepted without human or automated rule confirmation;
- AI outputs used for controlled decisions must be traceable to reviewed sources.

---

# 20. Quality Metrics

Use metrics to improve delivery, not to create bureaucracy.

Recommended metrics:

## Delivery

- lead time for change;
- deployment frequency;
- change failure rate;
- mean time to restore;
- release predictability;
- hotfix frequency.

## Engineering Quality

- build success rate;
- test pass rate;
- flaky test rate;
- code coverage trend;
- static analysis trend;
- escaped defects;
- reopened defects;
- failed deployment rate.

## Security

- critical/high vulnerabilities open;
- vulnerability age;
- dependency freshness;
- secret scan failures;
- security gate failures;
- accepted security risks nearing expiry.

## Operations

- deployment duration;
- rollback frequency;
- smoke test failure rate;
- error rate after deployment;
- incident correlation with deployment;
- environment drift.

## Process Health

- PR cycle time;
- review wait time;
- blocked work age;
- work-in-progress;
- unplanned work ratio;
- automation coverage;
- manual approval count by risk level.

Metrics should be reviewed periodically, not used as rigid individual performance targets.

---

# 21. What to Keep Strict

Even in the agile approach, the following must remain strict:

- code review before merge;
- automated tests before merge;
- protected main branch;
- secret scanning;
- dependency vulnerability scanning;
- authorization tests;
- tenant isolation tests;
- database migration validation;
- production deployment through controlled pipeline;
- production configuration from approved sources;
- backup and restore validation for critical data;
- monitoring and alerting for production services;
- rollback or forward-fix strategy;
- traceability from production release to included changes;
- audit logging for security-sensitive actions.

---

# 22. What to Keep Lightweight

The following should remain lightweight unless risk justifies more:

- formal approvals for normal stories;
- evidence packages for ordinary changes;
- full traceability matrices;
- manual gate meetings;
- electronic signatures;
- formal baselines for every iteration;
- release board for every small deployment;
- exhaustive documentation before development;
- waiver workflow for every non-critical test gap;
- manual test reports where automated results already exist.

---

# 23. Recommended Operating Cadence

## Daily

- developers work from short-lived branches;
- PRs reviewed quickly;
- CI validates changes;
- failing main branch treated as urgent;
- high-risk work discussed early.

## Per Sprint / Iteration

- deliver vertical slices;
- review automation gaps;
- remove flaky tests;
- review escaped defects;
- review deployment issues;
- refine test coverage for changed areas;
- update runbooks and docs only where needed.

## Per Release

- confirm release scope;
- run release candidate pipeline;
- deploy to staging;
- review security and migration risks;
- run smoke/synthetic checks;
- approve production deployment;
- monitor after release.

## Periodically

- review architecture drift;
- review test suite health;
- review dependency posture;
- rehearse backup/restore;
- rehearse rollback;
- prune obsolete tests;
- improve pipeline performance;
- review governance levels.

---

# 24. Recommended Initial Implementation Standard

For the first production-quality implementation phase, require:

1. Protected main branch.
2. Pull-request workflow.
3. Mandatory CI for every PR.
4. Unit tests for domain logic.
5. Integration tests for persistence, search, graph, eventing, and permissions.
6. Contract tests for public APIs and domain events.
7. Core end-to-end tests for main lifecycle journeys.
8. Automated security scanning.
9. Automated artifact build.
10. Deployment to a non-production environment.
11. Smoke tests after deployment.
12. Basic observability.
13. Issue-to-PR linkage.
14. Release notes for user-visible changes.
15. Production deployment through pipeline only.

This gives strong confidence without introducing a heavy assurance process.

---

# 25. Summary

The agile implementation and validation approach can be summarized as:

> Build in vertical slices.  
> Automate validation.  
> Keep governance proportional to risk.  
> Use tool-generated evidence by default.  
> Keep ordinary work lightweight.  
> Keep production, security, data, and tenant isolation strict.  
> Release frequently, observe continuously, and improve the process from real feedback.

This approach preserves the engineering discipline needed for a complex modular platform while avoiding unnecessary audit weight during normal agile development.
