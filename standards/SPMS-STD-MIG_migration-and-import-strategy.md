# Migration & Import Strategy Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-MIG |
| Component name | Migration & Import Strategy Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Engineering Integration Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | All module specifications that accept imports from external systems |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

Module specifications for `SPMS-REQ-MGMT`, `SPMS-TEST-VV`, `SPMS-CICD`, `SPMS-SEC-COMP`,
`SPMS-CFG-ASSET`, `SPMS-REL-DEP`, and `SPMS-DOC-KM` each mention import from spreadsheets,
issue trackers, requirement tools, Git repositories, CI/CD platforms, security scanners, and
CMDBs. Without a shared framework, each module would implement a different validation model,
ID mapping scheme, and rollback procedure.

This standard defines the **shared import pipeline** that all SPMS importers must implement,
eliminating duplication and ensuring consistent audit, traceability, and rollback behaviour
across all migration scenarios.

# 2. Source System Taxonomy

| Source type | Examples | Typical imported record types |
|---|---|---|
| Spreadsheet / CSV | Excel, Google Sheets | Requirements, issues, test cases, assets |
| Issue tracker | Jira, Linear, GitHub Issues, Azure DevOps | Issues, change requests, work packages |
| Requirement tool | DOORS, Polarion, Jama, Codebeamer | Requirements, test cases, trace links |
| Document repository | Confluence, SharePoint, Notion | Documents, knowledge articles |
| Git repository | GitHub, GitLab, Bitbucket | Commits, pull requests, branches, tags |
| CI/CD platform | Jenkins, GitHub Actions, GitLab CI, Tekton | Builds, pipelines, test results, artifacts |
| Security scanner | Trivy, Snyk, SonarQube, Dependency-Track | Vulnerabilities, scan reports, SBOMs |
| SBOM tool | Syft, CycloneDX tools | SBOMs, component inventories |
| CMDB | ServiceNow, i-doit | Configuration items, assets, topology |
| External SPMS instance | Another SPMS deployment | Any record type |

# 3. Import Pipeline

All importers must implement the following 5-stage pipeline in order. Stages must not be
skipped. Partial imports are not permitted — an import batch either commits in full or rolls
back entirely.

## Stage 1: Parse

**Objective:** Read source data; validate format; produce typed, normalised intermediate records.

- Detect source format (CSV column headers, JSON schema, XML namespace, API response shape).
- Map source fields to SPMS field names using the importer's field mapping configuration.
- Reject records with unrecognisable format with a clear error message identifying the source
  row/object and the failing field.
- Produce a normalised intermediate representation for all records before proceeding to
  Stage 2. Parse must not write to the SPMS database.

## Stage 2: Validate

**Objective:** Confirm that the normalised records are coherent and safe to import.

Validation checks (in order):
1. **Schema validation** — Required fields present; field types and lengths correct; enum values
   in allowed set; date formats valid.
2. **Referential integrity** — Referenced records (e.g., a requirement linked to a parent that
   must already exist) resolve to known SPMS IDs or to other records in the same import batch.
3. **Deduplication** — Identify records that already exist in SPMS (matched by source system ID
   from the ID mapping table, §4). Mark as `update` vs. `create` rather than rejecting.
4. **Conflict detection** — Identify records that would create conflicting state: duplicate
   titles where uniqueness is required, date overlaps, incompatible classifications.

Validation produces a **validation report**:
- Counts: records to create / update / skip / error.
- Per-error list: source row/id, field, error type, suggested resolution.
- Per-warning list: deduplication matches, classification changes, missing optional fields.

Validation failures at the error level must prevent the import from proceeding. Warnings do not
block the import but are included in the dry-run report.

## Stage 3: Map

**Objective:** Assign SPMS IDs to all incoming records; apply the ID mapping table.

- For each record to be created: allocate a new SPMS ID (`SPMS-STD-ID` scheme).
- For each record matched as a duplicate (`update`): retrieve the existing SPMS ID from the
  ID mapping table.
- Write new `source_system` + `source_id` → `spms_id` entries to the mapping table (§4).
  Mapping table writes are part of the import transaction — they are committed or rolled back
  with the import.
- ID mapping is idempotent: if the same `source_id` is imported again (re-sync), the existing
  mapping is returned without creating a new SPMS ID.

## Stage 4: Dry-run

**Objective:** Execute all preceding stages and produce a complete preview report without
committing any data.

The dry-run:
- Runs Stages 1–3 to completion.
- Simulates all database writes (creates, updates) and produces a change manifest:
  - Record-by-record list of intended operations (create / update / skip) with old and new
    field values.
  - Projected impact on trace links and baselines.
  - Validation report from Stage 2.
- Commits nothing to the database.
- Returns the dry-run report to the operator for review.

Dry-run must complete within the time bounds of `NFR-PERF-005` (≥ 10,000 records/hour,
`SPMS-STD-SCALE` §3) so that operators can review large imports in a reasonable time.

The dry-run report must be retained for the duration of the import session (minimum 24 hours)
and must produce an `AuditEvent` of type `ImportDryRunCompleted`.

## Stage 5: Commit or rollback

**Objective:** On operator confirmation, commit the full import atomically; otherwise abort.

**Commit path:**
1. Operator reviews the dry-run report and confirms (explicit approval action).
2. The import transaction is executed: all creates and updates from Stage 3 are committed to
   the relational store in a single database transaction.
3. Domain events (`IntegrationEvent`) are written to the outbox table in the same transaction
   for each created/updated record (`SPMS-STD-EVENT` §2.1).
4. The import batch is marked `committed` with timestamp and operator id.
5. An `AuditEvent` of type `ImportCommitted` is produced, including batch id, counts, and
   operator id.

**Rollback / abort path:**
- If the operator does not confirm, or if any commit-phase error occurs, the transaction is
  rolled back in full.
- An `AuditEvent` of type `ImportAborted` is produced.
- Partial commits are not permitted; the import is atomic.

# 4. ID Mapping Table

The ID mapping table persists the relationship between source system identifiers and SPMS IDs
for the lifetime of the integration. It is used for deduplication, re-sync, and audit
traceability.

| Field | Type | Required | Notes |
|---|---|---|---|
| `mapping_id` | string | Yes | Unique; immutable | — |
| `tenant_id` | string | Yes | Tenant scope | — |
| `source_system` | string | Yes | Canonical name of the source system (e.g., `jira`, `doors`, `github`) | — |
| `source_id` | string | Yes | Identifier in the source system | — |
| `spms_id` | string | Yes | SPMS record id assigned to this source record | — |
| `record_type` | string | Yes | SPMS record type | — |
| `component` | string | Yes | Owning SPMS component | — |
| `mapped_at` | timestamp | Yes | Immutable | — |
| `mapped_by` | string | Yes | Actor id (user or service) | — |
| `import_batch_id` | string | Yes | Id of the import batch that created this mapping | — |
| `notes` | string | No | Free text; e.g., migration notes or disambiguation | — |

The mapping table is itself a controlled record type; it must be retained for audit and re-sync.
Mapping entries are never deleted, only superseded (new mapping with updated `spms_id` if
a source record is merged or renamed).

# 5. Reconciliation for Live Integrations

For live integrations where source systems continue to change after initial import (CI/CD,
security scanners, Git, CMDB):

1. **Scheduled delta fetch** — The integration connector fetches changes since the last
   successful sync timestamp from the source system.
2. **Pipeline execution** — The same 5-stage pipeline runs on the delta, operating in
   non-interactive mode (dry-run report is logged but operator confirmation is not required for
   configured auto-reconciliation in Lightweight or Low-risk bulk governance profiles).
3. **Reconciliation report** — A report is produced and stored for each reconciliation run:
   records created, updated, skipped, errored; conflicts requiring manual review.
4. **Conflict escalation** — Conflicts that cannot be auto-resolved are raised as issues in
   `SPMS-ISS-CHG` for manual investigation.
5. **Audit trail** — Each reconciliation run produces `ImportCommitted` or `ImportAborted`
   `AuditEvent` records.

# 6. Post-Commit Rollback

A completed import batch may be rolled back if the following conditions are met:
- The rollback is requested within the configured retention window (default: 7 days).
- No record from the import batch has been included in a sealed `Baseline`.
- No record from the import batch has been referenced by a confirmed release or acceptance.

Rollback procedure:
1. The operator requests rollback of a specific `import_batch_id`.
2. The platform identifies all records created or updated in that batch (via `AuditEvent` log).
3. Created records are transitioned to `retired` state (never hard-deleted).
4. Updated records are reverted to their pre-import version (restored from the `Version` entity).
5. ID mappings from the batch are marked `superseded`.
6. An `AuditEvent` of type `ImportRolledBack` is produced, including batch id and operator id.

# 7. Cross-References

## 7.1 Module specifications using this standard

The following module specifications must comply with this standard for all import capabilities:

| Module | Import types |
|---|---|
| `SPMS-REQ-MGMT` | Spreadsheet, requirement tool (ReqIF), issue tracker |
| `SPMS-TEST-VV` | Spreadsheet, test framework results, requirement tool |
| `SPMS-CICD` | CI/CD platform events, build results, test results, artifact metadata |
| `SPMS-SEC-COMP` | Security scanner (SARIF), SBOM tools, vulnerability feeds |
| `SPMS-CFG-ASSET` | CMDB, cloud inventory, IaC state, Git/scanner discovery |
| `SPMS-REL-DEP` | CI/CD deployment events, release records from external systems |
| `SPMS-DOC-KM` | Document repository, spreadsheets, legacy document stores |

## 7.2 Related standards

| Standard | Relationship |
|---|---|
| `SPMS-DOMAIN-MODEL` §7.7 | `IntegrationEvent` outbox envelope written on import commit |
| `SPMS-STD-EVENT` | Outbox pattern applied on import commit |
| `SPMS-STD-ID` | SPMS ID format assigned to imported records |
| `SPMS-STD-SCALE` | `NFR-PERF-005` bounds import throughput (≥ 10,000 records/hour) |
| `SPMS-EVID-AUDIT` | `AuditEvent` produced at each pipeline stage boundary |
