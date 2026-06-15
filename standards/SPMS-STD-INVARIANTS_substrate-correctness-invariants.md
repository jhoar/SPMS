# Substrate Correctness Invariants Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-INVARIANTS |
| Component name | Substrate Correctness Invariants Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Platform Architecture Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | All substrate components: `SPMS-DATA-STORE`, `SPMS-EVID-AUDIT`, `SPMS-BASE-CCB`, `SPMS-TRACE-GRAPH`, `SPMS-INT-EVENT`, `SPMS-WF-GOV`, `SPMS-PLAT-CORE` |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

This standard names the substrate correctness invariants that must hold at all times during
normal system operation, defines a verification method for each, specifies the CI gate at which
each must become executable, and establishes that invariant failure is a blocking release issue.

The invariants in §2 complement the example-based smoke tests in `SPMS-THINTHREAD`. Where
`SPMS-THINTHREAD` validates specific, named end-to-end scenarios, this standard defines
property-based, continuous, and fuzz-based checks that must hold for all possible inputs and
states — not just the curated example set. Together they constitute the substrate correctness
gate for every phase exit from Phase 4 onward (when the graph substrate is complete), with
selected invariants active from earlier phases as specified.

This standard is the structural mitigation for `RISK-001` (substrate underestimated) and
`RISK-004` (graph↔relational consistency defects) in the `SPMS-DELIVERY` risk register.

# 2. Invariant Catalogue

Each invariant carries a stable identifier (`INV-NNN`) that must not be renumbered. The table
below summarises the catalogue; each subsection below provides the normative definition,
verification method, trigger, CI gate, and owning component.

| ID | Name | Owning Component | CI Phase Gate |
|---|---|---|---|
| `INV-001` | Audit append-only + hash chain | `SPMS-EVID-AUDIT` | Phase 3 |
| `INV-002` | Historical reconstruction fidelity | `SPMS-BASE-CCB`, `SPMS-EVID-AUDIT` | Phase 3 |
| `INV-003` | Graph↔relational consistency | `SPMS-TRACE-GRAPH`, `SPMS-DATA-STORE` | Phase 4 |
| `INV-004` | Baseline immutability | `SPMS-BASE-CCB` | Phase 3 |
| `INV-005` | Import reconciliation correctness | `SPMS-INT-EVENT`, `SPMS-DATA-STORE` | Phase 5 |
| `INV-006` | Permission-aware search consistency | `SPMS-PLAT-CORE`, `SPMS-DATA-STORE` | Phase 4 |
| `INV-007` | Event-projection convergence | `SPMS-INT-EVENT`, `SPMS-DATA-STORE` | Phase 5 |

---

### INV-001 Audit Append-Only + Hash Chain

**Invariant statement.** No `AuditEvent` record may be modified or deleted after creation. The
`prev_hash` field of each `AuditEvent` must equal the SHA-256 hash of the immediately preceding
`AuditEvent` record for the same tenant. Together these two properties constitute an immutable,
tamper-evident audit log per `SPMS-DOMAIN-MODEL §7.4` and `SPMS-STD-SEC §7`.

**Verification methods.**

1. *Property test — mutation rejection.* For a random sample of existing `AuditEvent` records,
   attempt UPDATE and DELETE via every supported data-access path (ORM, raw SQL, REST API,
   internal service call). Each attempt must be rejected with an appropriate error (HTTP 405 for
   REST; constraint violation at the database layer). No record may change.

2. *Scheduled chain validation.* A nightly job validates the full `prev_hash` chain for every
   active tenant: from the genesis event (where `prev_hash` is a fixed zero-hash sentinel) to the
   latest event. Any gap, mismatch, or unreachable predecessor is reported as a critical defect.

3. *Pre-export validation.* Before any audit package export (`SPMS-STD-SEC §7`), the exporting
   process must validate the chain for the requested tenant/period and abort if the chain is
   broken.

**Trigger.** Continuous (daily chain validation job); on-demand (pre-export, property-test suite).

**CI gate.** Phase 3 (when `SPMS-EVID-AUDIT` is delivered). Must pass at every phase exit from
Phase 3 onward.

---

### INV-002 Historical Reconstruction Fidelity

**Invariant statement.** For any controlled record and any point in time `T` in its history,
reconstructing the record's state as-of `T` must return exactly the fields, relationship links,
attached evidence, and lifecycle state that the record had at `T` — no later mutations may
appear, and no state that existed at `T` may be missing.

**Verification methods.**

1. *Property test — snapshot round-trip.* For N randomly selected (record, `past_time`) pairs
   drawn from active tenant data, assert:
   - Event-replay-derived state at `past_time` == `Version` snapshot captured at or immediately
     before `past_time` (per `SPMS-DOMAIN-MODEL §7.5`).
   - No field in the reconstructed snapshot has a value whose creation timestamp is later than
     `past_time`.
   - Every field present in the `Version` snapshot also appears in the event-replay result and
     vice versa.

2. *Baseline anchor test.* For every sealed `Baseline`, reconstructing each member record at
   `sealed_at` must return the version captured in `Baseline.members` verbatim.

**Trigger.** On-demand (property-test suite); nightly regression pass over a rolling 30-day
sample window.

**CI gate.** Phase 3 (when `SPMS-BASE-CCB` and `SPMS-EVID-AUDIT` are delivered). Must pass at
every phase exit from Phase 3 onward.

---

### INV-003 Graph↔Relational Consistency

**Invariant statement.** At any point after a transaction commits, the set of active `TraceLink`
records in the relational store and the set of edges in the graph projection must be identical:
equal counts, equal source/target endpoint identifiers, equal link types, and equal `suspect`
flags. No active link may appear in one store and not the other.

**Verification methods.**

1. *Rebuild-and-compare.* A nightly job runs a full graph rebuild from the relational store
   (`SPMS-STD-EVENT §7`, rebuild protocol) and then performs a set-difference comparison between
   the rebuilt graph edges and the live graph projection. Any divergence (edge present in
   relational but absent from graph, or vice versa) is a blocking defect.

2. *Count-parity assertion.* After every `TraceLink` create, update, or delete operation,
   a synchronous assertion checks that the relational `TraceLink` count for the affected tenant
   equals the graph edge count within the consistency window defined in `SPMS-STD-EVENT §7.3`.
   Divergence beyond the window is escalated to a blocking defect.

**Trigger.** Continuous (nightly rebuild-and-compare); post-mutation assertion.

**CI gate.** Phase 4 (when `SPMS-TRACE-GRAPH` is delivered and the graph substrate is complete).
Must pass at every phase exit from Phase 4 onward.

---

### INV-004 Baseline Immutability

**Invariant statement.** Once a `Baseline` record transitions to the `sealed` state, its
`members` set (the list of record IDs and their captured version IDs) must never change, and
each captured `Version` snapshot must remain retrievable verbatim for the retention period.

**Verification methods.**

1. *Property test — mutation rejection.* Attempt to add, remove, or modify any member in a
   sealed `Baseline` via every supported data-access path. Each attempt must be rejected with
   HTTP 422 (per `SPMS-THINTHREAD` TGT-005 acceptance criterion A5). No member set may change.

2. *Version integrity check.* A periodic job (weekly minimum) computes and compares the hash of
   each captured `Version` snapshot against the hash recorded at capture time. Any mismatch is
   a critical defect.

**Trigger.** On-demand (property-test suite); weekly integrity check.

**CI gate.** Phase 3 (when `SPMS-BASE-CCB` is delivered). Must pass at every phase exit from
Phase 3 onward.

---

### INV-005 Import Reconciliation Correctness

**Invariant statement.** After an import commit completes via the `SPMS-STD-MIG` pipeline:
(a) the ID-mapping table is bijective per source system (no source ID maps to two SPMS IDs,
and no SPMS ID is claimed by two source IDs); (b) re-running the same import payload is
idempotent (no duplicate records are created, and no existing records are overwritten without an
explicit reconciliation decision); (c) executing the post-commit rollback (`SPMS-STD-MIG §6`)
returns the database to a state identical to the pre-import snapshot.

**Verification methods.**

1. *Pipeline property test.* Execute the full five-stage import pipeline (`SPMS-STD-MIG §3–6`)
   against a synthetic dataset of known size. Assert bijectivity of the resulting ID-mapping
   table. Re-run with the identical payload and assert zero new records.

2. *Dry-run/commit parity.* For each import, the record count reported in the dry-run preview
   must equal the record count created in the commit stage. Discrepancies are a blocking defect.

3. *Rollback fidelity test.* After commit on a synthetic dataset, execute rollback and compare
   the post-rollback database state against a snapshot taken before the import. Any difference
   is a blocking defect.

**Trigger.** On-demand (property-test suite); executed before each release candidate that
includes the migration pipeline.

**CI gate.** Phase 5 (when `SPMS-INT-EVENT` and the full import pipeline are delivered). Must
pass at every phase exit from Phase 5 onward.

---

### INV-006 Permission-Aware Search Consistency

**Invariant statement.** No search result, graph traversal response, or report projection may
return a record or field value that the requesting actor is not authorised to read under the
six-layer ABAC/RBAC evaluation defined in `SPMS-STD-SEC §3`. Conversely, every record the
actor is authorised to read and that matches the search criteria must appear in results (no
incorrect redaction). Tenant isolation means a cross-tenant actor must receive HTTP 400 (not
403 or 404) when accessing data outside their tenant scope (`SPMS-THINTHREAD` TGT-010).

**Verification methods.**

1. *Property test — projection visibility.* For N randomly selected (actor, record) pairs, assert
   that the record's presence in search/graph/report output exactly matches the authoritative
   ABAC/RBAC decision computed directly for that actor-record pair (`SPMS-STD-SEC §3`). Neither
   over-exposure nor under-exposure is acceptable.

2. *Tenant-isolation fuzz test.* Automated fuzzing with synthetic cross-tenant actors attempts
   to retrieve records from tenant A while authenticated as tenant B. Every such attempt must
   return HTTP 400. This extends the acceptance criterion of `SPMS-THINTHREAD` TGT-010.

3. *Field-level redaction audit.* For classification-restricted fields, verify that redacted
   output (the `[REDACTED]` sentinel per `SPMS-STD-SEC §4`) appears in projection output where
   the actor lacks field-read permission, and the raw value never appears.

**Trigger.** On-demand (property-test suite); continuous (nightly fuzz run).

**CI gate.** Phase 4 (when the graph substrate and search projection are integrated). Must pass
at every phase exit from Phase 4 onward.

---

### INV-007 Event-Projection Convergence

**Invariant statement.** Replaying the complete ordered event log for a tenant onto an empty
projection yields a projection state equal to the live projection state, within the eventual
consistency bound defined as NFR-PERF-006 in `SPMS-STD-SCALE`. Projection checkpoint sequence
numbers must be monotonically increasing and must never regress.

**Verification methods.**

1. *Rebuild-and-compare.* Execute a full projection rebuild from the event log (per
   `SPMS-STD-EVENT §7`) for a test tenant. Compare every projection record against the live
   projection. Any field-level divergence is a blocking defect.

2. *Checkpoint monotonicity assertion.* After every event batch is processed, assert that each
   projection's last-processed sequence number is strictly greater than the previous value.
   Any regression triggers an immediate alert and blocks further processing until resolved.

**Trigger.** Continuous (nightly rebuild-and-compare); post-deploy smoke (checkpoint assertion).

**CI gate.** Phase 5 (when `SPMS-INT-EVENT` and the event bus are in place). Must pass at every
phase exit from Phase 5 onward.

---

# 3. Test Classes

The verification methods in §2 belong to the following three test classes. Each class maps to a
layer in the test pyramid defined in `agile_implementation_and_validation_approach` and to a
pipeline stage.

| Test class | Invariants | Pipeline stage | Trigger |
|---|---|---|---|
| Property-based / invariant tests | INV-001 (mutation rejection), INV-002, INV-004, INV-005, INV-006 | Unit + integration | On-demand; nightly |
| Rebuild-and-compare jobs | INV-001 (chain validation), INV-003, INV-007 | Nightly pipeline | Scheduled |
| Fuzz / isolation tests | INV-006 (tenant fuzz) | Nightly pipeline; RC gate | Scheduled; pre-release |

**Property-based tests** generate large random input spaces over the specific invariant
predicate. They must use a reproducible seed for CI (to allow replay of failures) and a random
seed for scheduled nightly runs (to broaden coverage over time).

**Rebuild-and-compare jobs** are full-pipeline exercises: they spin up a clean projection store,
replay the event log or rebuild from relational data, then perform field-level comparison.
Differences are reported as blocking defects, not warnings.

**Fuzz tests** for tenant isolation use a corpus of synthetic tenants and cross-tenant actors
generated at test-data initialisation time. The corpus must include at least 3 tenants with
overlapping record types to ensure isolation boundaries are stress-tested.

# 4. CI Gates and Phase Gates

| Phase | Invariants that must pass from this phase exit onward |
|---|---|
| Phase 3 exit | INV-001, INV-002, INV-004 |
| Phase 4 exit | INV-001, INV-002, INV-003, INV-004, INV-006 |
| Phase 5 exit and all subsequent | INV-001, INV-002, INV-003, INV-004, INV-005, INV-006, INV-007 |

An invariant check failure at a phase gate is a **blocking release issue** with the same
severity as a regression in `SPMS-THINTHREAD`. It must be resolved before the phase is marked
complete. No waiver may be granted for an invariant failure without explicit Engineering Director
approval and a documented resolution plan with a deadline.

Each invariant check must be:
- Executable in an automated CI environment without manual intervention.
- Reproducible: the same code and data state must always produce the same pass/fail outcome.
- Attributable: failures must identify the specific invariant, the input that triggered it, the
  expected state, and the observed state.

# 5. Ownership

| Invariant | Primary owning component | Supporting component | Governing spec section |
|---|---|---|---|
| INV-001 | `SPMS-EVID-AUDIT` | — | `SPMS-STD-SEC §7`; `SPMS-DOMAIN-MODEL §7.4` |
| INV-002 | `SPMS-BASE-CCB` | `SPMS-EVID-AUDIT` | `SPMS-DOMAIN-MODEL §7.5` |
| INV-003 | `SPMS-TRACE-GRAPH` | `SPMS-DATA-STORE` | `SPMS-STD-EVENT §7.3` |
| INV-004 | `SPMS-BASE-CCB` | — | `SPMS-THINTHREAD` TGT-005 |
| INV-005 | `SPMS-INT-EVENT` | `SPMS-DATA-STORE` | `SPMS-STD-MIG §3–6` |
| INV-006 | `SPMS-PLAT-CORE` | `SPMS-DATA-STORE` | `SPMS-STD-SEC §3–4` |
| INV-007 | `SPMS-INT-EVENT` | `SPMS-DATA-STORE` | `SPMS-STD-EVENT §4`, §7 |

The owning component team is responsible for: maintaining the executable check, triaging
failures, and escalating blocking defects via the change-control process in `SPMS-BASE-CCB`.

# 6. Cross-References

| Document | Relationship |
|---|---|
| `SPMS-THINTHREAD` | Example-based smoke tests (TGT-001–010); INV-004 and INV-006 extend TGT-005 and TGT-010 respectively |
| `SPMS-STD-EVENT` | Transactional outbox model, rebuild protocol (`§7`), projection consistency window (`§7.3`) |
| `SPMS-STD-SEC` | Audit log tamper resistance (`§7`); ABAC/RBAC evaluation order (`§3`); field-level security (`§4`) |
| `SPMS-STD-MIG` | Import pipeline stages (`§3–6`); post-commit rollback (`§6`) |
| `SPMS-DOMAIN-MODEL §7` | Canonical entity schemas: AuditEvent (`§7.4`), Version/Baseline (`§7.5`), TraceLink (`§7.6`) |
| `SPMS-EVID-AUDIT §9` | Audit package export and chain validation |
| `SPMS-BASE-CCB` | Baseline sealing, member immutability, version snapshot lifecycle |
| `SPMS-STD-SCALE` | NFR-PERF-006 (eventual consistency bound for INV-007) |
| `SPMS-DELIVERY` | RISK-001 (substrate underestimated); RISK-004 (graph↔relational consistency) |

# 7. Governance, Approvals, Waivers, and Gates

A waiver against any invariant in this standard requires:
1. A written justification identifying the invariant, the specific check being waived, and the
   technical reason it cannot pass in the given context.
2. A time-bounded remediation plan with a named owner and a deadline no later than the following
   phase exit.
3. Sign-off by the Engineering Director and the Programme Technical Authority.

Waivers are recorded as `AuditEvent` records of type `WaiverGranted` against the owning
component and must be reviewed at each phase boundary.

No waiver may remain open across two consecutive phase exits.

# 8. Evidence, Audit, and Historical Reconstruction

All invariant check results (pass/fail, timestamp, invariant ID, input seed, comparison
summary) must be recorded as structured log entries in the CI system and retained for the
programme audit retention period.

Invariant check result records are themselves immutable once written (append-only log). They
are subject to the same historical reconstruction guarantee as controlled records: given an
invariant check run ID, the full input parameters and output must be reconstructable.
