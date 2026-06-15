# Delivery Methodology Reconciliation Note

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-METHODOLOGY |
| Component name | Delivery Methodology Reconciliation Note |
| Component type | Programme standard |
| Version | 1.0 |
| Status | Approved for reconciled set v1 |
| Owner | Programme Technical Authority |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |
| Governs | `phase-implementation-plan.md` and `agile_implementation_and_validation_approach.md` |

---

# 1. The conflict being resolved

The two planning documents appeared to contradict each other:

- The **Phase Implementation Plan** lists, as explicit non-negotiables, "No MVP" and
  "No vertical slice", and mandates a foundation-first build with full evidence, audit, security,
  and acceptance criteria in every phase.
- The **Agile Implementation and Validation Approach** states the opposite: "The preferred delivery
  pattern is vertical slicing", "Avoid building all backend first", and "Formal evidence packs
  should not be required for ordinary development work."

Read literally, a team following one document violates the other. The underlying intentions are in
fact compatible; the documents were using the same words for different scopes. This note states the
reconciled position, which both documents now reference.

# 2. Two different axes, not a contradiction

**Axis 1 — macro sequencing (what gets built before what).** Here the Phase Plan governs. The
shared substrate (kernel, workflow/governance, evidence/audit, baseline, traceability, search,
events, persistence) is built before the functional modules that depend on it. "No MVP" means the
product does not ship as a bare ticket tracker with governance bolted on later. "No vertical slice"
**at this level** means no single business module is driven end-to-end to feature-completeness
before the substrate it relies on exists.

**Axis 2 — micro construction (how each increment is built).** Here the Agile Approach governs.
*Within* a phase or increment, work is delivered as thin vertical slices — domain model, API,
persistence, permissions, workflow, UI, events, tests, deployment, observability — rather than all
backend first, then all UI. This is the normal meaning of "vertical slice" in agile practice and is
not in conflict with Axis 1.

So: **foundation-first across phases; vertical slices within each phase.** The word "vertical
slice" is reserved hereafter for Axis 2. The Phase Plan's prohibition is reworded to
"no premature end-to-end module before its substrate" to remove the collision.

# 3. Governance is a product feature, built under a lightweight process

The second apparent conflict — heavy governance in the Phase Plan versus lightweight governance in
the Agile Approach — dissolves on the same distinction:

- The **system being built** must implement strong governance (approvals, gates, evidence,
  baselines, immutable audit, waivers). That is product scope and is not negotiable.
- The **process of building the system** applies governance proportional to risk, using the three
  governance levels in the Agile Approach. Producing the evidence service does not require a formal
  evidence pack for every commit that touches it.

The strict list in the Agile Approach (code review, automated tests, protected main, secret/
dependency scanning, authorization and tenant-isolation tests, migration validation, controlled
production deployment, backup/restore validation, audit logging of security-sensitive actions)
remains mandatory at all times and is consistent with the Phase Plan's per-phase requirements,
which are satisfied by automated tool-generated evidence rather than manual paperwork.

# 4. Reconciled rule (authoritative)

1. Sequence phases foundation-first per the Phase Plan.
2. Build each increment as a vertical slice per the Agile Approach.
3. Apply governance levels 1–3 to the construction process by risk.
4. Hold production safety, security, tenant isolation, data integrity, and reversibility strict at
   all times regardless of governance level.
5. Where the two documents still read as conflicting after this note, this note governs.

# 5. Practical consequence: the thin governed thread

A direct consequence is the "thin governed thread" first increment described in `SPMS-DELIVERY`.
After the kernel exists, one record type is carried end-to-end (create → review → approve →
baseline → evidence → trace → audit) as a single vertical slice. This proves the substrate against
real usage early, gives stakeholders something demonstrable before the functional modules arrive,
and honours both documents: it is a vertical slice (Axis 2) that does not jump ahead of the
substrate (Axis 1).
