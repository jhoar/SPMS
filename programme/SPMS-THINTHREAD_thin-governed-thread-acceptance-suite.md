# Thin Governed Thread Acceptance Suite

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-THINTHREAD |
| Component name | Thin Governed Thread Acceptance Suite |
| Component type | Programme document (acceptance test specification) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and delivery plan, see: `SPMS-INDEX` (register),
> `SPMS-DELIVERY`, and `SPMS-METHODOLOGY`.

# 1. Purpose

The thin governed thread is defined in `SPMS-DELIVERY` (lines 53–72) and reconciled in
`SPMS-METHODOLOGY` (lines 81–88) as the earliest vertical slice through the SPMS substrate:
one controlled record type carried end-to-end through the full governance loop to prove the
substrate against real usage before functional modules are built.

This document formalises the thin governed thread as a **named, executable acceptance test
suite** of 10 scenarios (`TGT-001` through `TGT-010`).

**Invariant status:** This suite is the smoke test for every phase exit from Phase 2 onward.
All 10 scenarios must pass at the exit of Phase 2 and must continue to pass at the exit of
every subsequent phase (3–12). Regression of any scenario is a **blocking release issue** —
not a known issue, not a deferred defect. Phase exit criteria in `SPMS-DELIVERY` are read as
implicitly including "TGT-001 through TGT-010 all pass."

The suite must be included in the CI/CD pipeline from Phase 2 onward and must be re-run on
every release candidate.

# 2. Scope

The suite uses one controlled record type: **Controlled Item** (generic; no functional module
semantics required). It exercises only the substrate components:

| Substrate component | Capability exercised |
|---|---|
| `SPMS-PLAT-CORE` | Tenant and user identity; record creation and retrieval; permission enforcement |
| `SPMS-WF-GOV` | Lifecycle transitions (Draft → In Review → Approved); approval workflow |
| `SPMS-EVID-AUDIT` | Evidence attachment; AuditEvent emission and retrieval |
| `SPMS-BASE-CCB` | Baseline creation; record membership; immutable snapshot |
| `SPMS-TRACE-GRAPH` | Trace link creation; suspect link detection |
| `SPMS-INT-EVENT` | Domain event emission; outbox relay; projection consumer processing |
| `SPMS-DATA-STORE` | Relational store persistence; search index update; historical reconstruction |

No functional module records (`SPMS-REQ-MGMT`, `SPMS-ISS-CHG`, etc.) are used. If functional
modules are present in the deployment, their record types must not be required for any scenario
in this suite to pass.

# 3. Prerequisites

The following conditions must be satisfied before running the suite:

| # | Prerequisite |
|---|---|
| P-1 | A running SPMS deployment with at minimum the 7 substrate components listed in §2. |
| P-2 | One tenant (`tenant_id = TGT-TENANT`) configured and active. |
| P-3 | One project (`project_id = TGT-PROJECT`) in `TGT-TENANT`, configured with Standard governance profile. |
| P-4 | One user (`user_id = TGT-USER-A`) in `TGT-TENANT` with Owner and Approver roles for `TGT-PROJECT`. |
| P-5 | A second tenant (`tenant_id = TGT-TENANT-B`) with one user (`user_id = TGT-USER-B`) who has no permissions in `TGT-TENANT`. |
| P-6 | The event bus is running and at least one projection consumer (search index or reporting) is active and subscribed. |
| P-7 | A test harness can call the SPMS API as `TGT-USER-A` and as `TGT-USER-B`. |
| P-8 | All prerequisite infrastructure is in a known-clean state (no pre-existing Controlled Items, baselines, or trace links from previous runs — or the harness operates in an isolated test project/tenant). |

# 4. Test Scenarios

Each scenario is specified as: ID, Title, Given/When/Then steps, Assertions, and Pass criteria.

---

## TGT-001 — Create a Controlled Item

**Title:** Create a new Controlled Item in Draft state.

**Given:** Prerequisites P-1 through P-7 are satisfied; TGT-TENANT contains no Controlled Items.

**When:** `TGT-USER-A` calls the record creation API to create a Controlled Item with title
"Thread Item Alpha", `classification = internal`, in `TGT-PROJECT`.

**Then:**
1. The API returns HTTP 201 with a record body.
2. The returned record has a valid SPMS id matching the `SPMS-STD-ID` format.
3. `tenant_id = TGT-TENANT`, `project_id = TGT-PROJECT`.
4. `lifecycle_state = draft`.
5. `version = 1`.
6. `owner_id = TGT-USER-A`.

**Assertions:**
- A1: Record is retrievable by id and returns identical field values.
- A2: An `AuditEvent` of type `RecordCreated` exists with `aggregate_id` = the new record id,
  `actor_id = TGT-USER-A`, `tenant_id = TGT-TENANT`.
- A3: An `IntegrationEvent` of type `RecordCreated` with `status` in (`pending` or `published`)
  exists in the outbox for the new record id.

**Pass criteria:** All of A1–A3 are satisfied; no errors raised.

---

## TGT-002 — Submit for Review

**Title:** Transition the Controlled Item from Draft to In Review.

**Given:** TGT-001 has passed; the Controlled Item ("Thread Item Alpha") is in `draft` state.

**When:** `TGT-USER-A` calls the workflow transition API with trigger `submit_for_review` on
the Controlled Item.

**Then:**
1. The API returns HTTP 200.
2. The record's `lifecycle_state` is now `in_review`.
3. The record's `version` is incremented to 2.

**Assertions:**
- A1: Record retrieved by id shows `lifecycle_state = in_review`, `version = 2`.
- A2: An `AuditEvent` of type `StateChanged` exists with `from_state = draft`,
  `to_state = in_review`, `actor_id = TGT-USER-A`.
- A3: At least one notification was queued for the reviewer role in `TGT-PROJECT` (notification
  record exists or notification event emitted; exact delivery mechanism is deployment-dependent).

**Pass criteria:** A1 and A2 are satisfied; A3 is satisfied where notifications are enabled.

---

## TGT-003 — Approve the Record

**Title:** Approve the Controlled Item; confirm approval record and audit event.

**Given:** TGT-002 has passed; the Controlled Item is in `in_review` state.

**When:** `TGT-USER-A` (holding the Approver role) calls the approval API to approve the
Controlled Item with notes "Approved for thread test".

**Then:**
1. The API returns HTTP 200.
2. The record's `lifecycle_state` is now `approved`.
3. An Approval entity is created.

**Assertions:**
- A1: Record shows `lifecycle_state = approved`, `version = 3`.
- A2: An `Approval` record exists with `record_id` = Thread Item Alpha id, `status = approved`,
  `decisions[0].approver_id = TGT-USER-A`, `decisions[0].decision = approved`.
- A3: An `AuditEvent` of type `ApprovalCompleted` exists with `actor_id = TGT-USER-A`.
- A4: An `AuditEvent` of type `StateChanged` exists with `from_state = in_review`,
  `to_state = approved`.

**Pass criteria:** A1–A4 are all satisfied.

---

## TGT-004 — Attach Evidence

**Title:** Attach an evidence record to the approved Controlled Item.

**Given:** TGT-003 has passed; the Controlled Item is in `approved` state.

**When:** `TGT-USER-A` attaches an evidence record of type `document` with title
"Approval Notes", linking it to the Controlled Item. (Evidence content may be a
synthetic/placeholder object.)

**Then:**
1. The API returns HTTP 201.
2. An Evidence entity is created.

**Assertions:**
- A1: An `Evidence` record exists with `record_id` = Thread Item Alpha id,
  `evidence_type = document`, `status = valid`, `uploaded_by = TGT-USER-A`.
- A2: An `AuditEvent` of type `EvidenceAttached` exists with `aggregate_id` = Thread Item
  Alpha id, `actor_id = TGT-USER-A`.

**Pass criteria:** A1–A2 are satisfied.

---

## TGT-005 — Create a Baseline

**Title:** Create a baseline containing the approved Controlled Item; confirm immutable snapshot.

**Given:** TGT-004 has passed; the Controlled Item is in `approved` state with attached evidence.

**When:** `TGT-USER-A` creates a Baseline named "Thread Baseline v1" with the Controlled Item
(at its current version) as a member.

**Then:**
1. The API returns HTTP 201.
2. A Baseline entity is created with `status = sealed`.

**Assertions:**
- A1: `Baseline` record exists with `name = Thread Baseline v1`, `status = sealed`,
  `members` contains `{record_id: <Thread Item Alpha id>, version: 3}`.
- A2: The Controlled Item's `baseline_refs` array includes the new baseline id.
- A3: The baseline `sealed_at` and `sealed_by` fields are set.
- A4: An `AuditEvent` of type `BaselineMembershipChanged` exists.
- A5: Attempting to delete or modify the `members` list of the sealed baseline via the API
  returns HTTP 422 (immutability enforced).

**Pass criteria:** A1–A5 are satisfied.

---

## TGT-006 — Create a Trace Link and Confirm Graph Projection

**Title:** Link two Controlled Items; confirm the trace link appears in the graph projection.

**Given:** TGT-005 has passed; Thread Item Alpha is baselined and approved. A second Controlled
Item ("Thread Item Beta") has been created in `approved` state in `TGT-PROJECT` (creation
steps follow TGT-001 through TGT-003 for Beta; these steps may be pre-executed as setup).

**When:** `TGT-USER-A` creates a trace link of type `depends-on`
(`SPMS-TRACE-GRAPH-REL-007`) from Thread Item Beta to Thread Item Alpha.

**Then:**
1. The API returns HTTP 201.
2. A `TraceLink` entity is created.

**Assertions:**
- A1: `TraceLink` record exists with `source_id = Thread Item Beta id`,
  `target_id = Thread Item Alpha id`, `link_type = SPMS-TRACE-GRAPH-REL-007`,
  `suspect = false`.
- A2: The graph projection (queried via the traceability API) returns the link when traversing
  from Thread Item Beta.
- A3: An `AuditEvent` of type `LinkCreated` exists.
- A4: The coverage metric for Thread Item Alpha (or the project's graph coverage score) is
  updated in the projection (non-zero; exact value is deployment-dependent).

**Pass criteria:** A1–A3 are satisfied; A4 is satisfied where coverage metrics are enabled.

---

## TGT-007 — Trigger Suspect Link Detection

**Title:** Update the source record after linking; confirm the dependent link is marked suspect.

**Given:** TGT-006 has passed; Thread Item Beta depends-on Thread Item Alpha; Thread Item Alpha
is in `approved` state at version 3.

**When:** `TGT-USER-A` updates a metadata field on Thread Item Alpha (e.g., description),
causing a new version to be committed.

**Then:**
1. The API returns HTTP 200.
2. Thread Item Alpha is now at version 4.

**Assertions:**
- A1: The `TraceLink` from Thread Item Beta to Thread Item Alpha now has `suspect = true`.
- A2: `suspect_reason` is set on the link (non-empty string).
- A3: An `AuditEvent` or notification event exists indicating suspect link propagation for
  Thread Item Beta.

**Pass criteria:** A1–A2 are satisfied; A3 is satisfied where suspect-link notifications are
enabled.

---

## TGT-008 — Event Propagation to Search Projection

**Title:** Confirm that a domain event from a record update is processed by the search projection.

**Given:** TGT-001 through TGT-007 have produced multiple events. Thread Item Alpha has a
unique title ("Thread Item Alpha") not present in any other record.

**When:** The test harness waits for the outbox relay to publish and the search consumer to
process all pending events (maximum wait: 120 s, consistent with `NFR-PERF-006` × 2).

**Then:**
1. The search index has been updated.

**Assertions:**
- A1: A search query for "Thread Item Alpha" (title search, `TGT-PROJECT` scope) returns
  Thread Item Alpha as a result with the correct record id and current `lifecycle_state`.
- A2: An `IntegrationEvent` for the most recent `RecordUpdated` event on Thread Item Alpha
  has `status = published` (relay has confirmed delivery).

**Pass criteria:** A1–A2 are satisfied within the wait bound.

---

## TGT-009 — Historical Reconstruction at Baseline

**Title:** Reconstruct Thread Item Alpha's state at the point of baseline creation.

**Given:** TGT-005 has passed. Thread Item Alpha is now at version 4 (updated in TGT-007).
Thread Baseline v1 captured Thread Item Alpha at version 3.

**When:** `TGT-USER-A` calls the historical reconstruction API requesting the state of Thread
Item Alpha at the `sealed_at` timestamp of Thread Baseline v1.

**Then:**
1. The API returns a historical snapshot.

**Assertions:**
- A1: The returned snapshot has `version = 3`, `lifecycle_state = approved`.
- A2: The snapshot includes the evidence reference added in TGT-004.
- A3: The snapshot does not include changes made in TGT-007 (version 4 changes are not visible).
- A4: An `AuditEvent` of type `HistoricalReconstructionPerformed` (or equivalent) is emitted,
  recording the actor and the reconstruction point-in-time.

**Pass criteria:** A1–A3 are satisfied; A4 is satisfied where reconstruction auditing is enabled.

---

## TGT-010 — Tenant Isolation Enforcement

**Title:** Confirm that a user from a different tenant cannot access or approve Thread Item Alpha.

**Given:** TGT-001 has passed. `TGT-USER-B` is a valid authenticated user in `TGT-TENANT-B`
and has no permissions in `TGT-TENANT`.

**When (a):** `TGT-USER-B` calls the record retrieval API for Thread Item Alpha's id.

**Then (a):**
1. The API returns HTTP 400 (tenant mismatch — protocol error per `SPMS-STD-SEC` §2.1), not
   HTTP 403 or HTTP 404.

**When (b):** `TGT-USER-B` calls the approval API for Thread Item Alpha.

**Then (b):**
1. The API returns HTTP 400.
2. No `AuditEvent` of type `ApprovalCompleted` is emitted for Thread Item Alpha by
   `TGT-USER-B`.
3. Thread Item Alpha's `lifecycle_state` is unchanged.

**Assertions:**
- A1: Both API calls in (a) and (b) return HTTP 400.
- A2: Thread Item Alpha is not modified.
- A3: No cross-tenant `AuditEvent` is emitted with `actor_id = TGT-USER-B`.

**Pass criteria:** A1–A3 are satisfied.

---

# 5. Invariant Status and CI Integration

## 5.1 Inclusion in CI/CD pipeline

From Phase 2 completion onward, the acceptance suite must be:
- Included in the **per-release-candidate pipeline** (`agile_implementation_and_validation_approach` §8.4).
- Run against a **staging or integration environment** — not against a unit-test mock.
- Executed using the production-equivalent substrate configuration (same workflow definitions,
  governance profile, and event bus as production).

## 5.2 Regression handling

Any new phase increment that causes one or more TGT scenarios to fail must:
1. Block the phase exit gate (not waiveable without Programme Technical Authority approval).
2. Produce a linked issue in `SPMS-ISS-CHG` (once that module is available) or a tracked
   incident otherwise.
3. Be resolved before the phase increment is released to staging or production.

## 5.3 Extension

Additional scenarios may be added to this suite as functional modules are built (e.g.,
TGT-011 testing requirement-to-test-case traceability when `SPMS-REQ-MGMT` and `SPMS-TEST-VV`
are deployed). Extensions are Level 2 controlled changes to this document. The 10 core scenarios
(`TGT-001` through `TGT-010`) must never be removed or weakened.
