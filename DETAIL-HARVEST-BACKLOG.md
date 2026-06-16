# Detail Harvest Backlog

| Field | Value |
|---|---|
| Owner | Programme Technical Authority |
| Status | Open (High-priority items cleared) |
| Last updated | 2026-06-16 |

## Purpose

Reconciliation kept the named set as the canonical module/functional layer and superseded the
numbered set. Several superseded numbered specs were larger and carried net-new detail (extra
entities, attributes, capabilities) that is worth incorporating into the canonical specs during
each component's detailed-design phase. This backlog tracks that harvest so the detail is not lost.
The superseded files remain read-only in `_superseded/` until each item is cleared or deferred.

## How to use

Before a component enters detailed design (per the Phase Implementation Plan), the owner diffs the
canonical spec against the listed superseded source, lifts any genuinely additional and correct
detail into the canonical spec under the global ID scheme (`SPMS-STD-ID`), and marks the item done.

## Backlog

| Item | Canonical target | Superseded source(s) | Net-new detail to review | Priority | Status |
|---|---|---|---|---|---|
| H-01 | `SPMS-REL-DEP` | `SPMS-FUN-011` | Additional entities (`Version`, `ReleaseScopeItem`, `ReleaseBaseline`), extra capabilities (scope/change control, build-artifact linkage) | High (Phase 9) | Done (2026-06-16) |
| H-02 | `SPMS-CFG-ASSET` | `SPMS-FUN-012` | Fuller asset/CI attribute set and drift detail | High (Phase 9) | Done (2026-06-16) |
| H-03 | `SPMS-SEC-COMP` | `SPMS-FUN-013`, `SPMS-SUB-010` (security) | Expanded control/vulnerability/threat-model detail; security-ops items from SUB-010 | High (Phase 10) | Done (2026-06-16) |
| H-04 | `SPMS-PROD-ASSUR` | `SPMS-FUN-014` | Expanded NCR/CAPA/assurance-gate detail | Medium (Phase 10) | Open |
| H-05 | `SPMS-REPORT-ANALYTICS` | `SPMS-FUN-015`, `SPMS-SUB-007` | Search/query/saved-view detail from SUB-007; extra metric definitions | Medium (Phase 5/11) | Open |
| H-06 | `SPMS-AUTO-AI` | `SPMS-FUN-016` | Extra grounding/evaluation/red-team detail | Medium (Phase 12) | Open |
| H-07 | `SPMS-PLAT-CORE` | `SPMS-SUB-001`, `SPMS-SUB-002`, `SPMS-SUB-010` | Detailed RBAC/ABAC/field-level rules (001), full record-model attribute set (002), admin/retention/observability (010) | High (Phase 1) | Done (2026-06-16) |
| H-08 | `SPMS-WF-GOV` | `SPMS-SUB-003` | Quorum/parallel/conditional approval detail; e-signature metadata | High (Phase 2) | Done (2026-06-16) |
| H-09 | `SPMS-TRACE-GRAPH` | `SPMS-SUB-004` | Cardinality/validity rules per link type; suspect-link propagation detail | High (Phase 4) | Done (2026-06-16) |
| H-10 | `SPMS-EVID-AUDIT` | `SPMS-SUB-005` | Immutable-log mechanics; evidence-package composition detail | High (Phase 3) | Done (2026-06-16) |
| H-11 | `SPMS-BASE-CCB` | (already promoted from `SPMS-SUB-006`) | None — promoted whole; review only for ID consistency | Low | Open |
| H-12 | `SPMS-INT-EVENT` | (already promoted from `SPMS-SUB-008`) | None — promoted whole; confirm event contracts vs `SPMS-DOMAIN-MODEL` | Low | Open |
| H-13 | `SPMS-DATA-STORE` | (already promoted from `SPMS-SUB-009`) | None — promoted whole; confirm storage choices vs `SPMS-STD-SCALE` | Low | Open |

Note: the six core operational modules (`WP-PLAN`, `ISS-CHG`, `DOC-KM`, `REQ-MGMT`, `TEST-VV`,
`CICD`) had no numbered-set counterpart, so there is nothing to harvest for them.

## Harvest log

**2026-06-16 — High-priority items H-01, H-02, H-03, H-07, H-08, H-09, H-10 cleared.**

Net-new detail was lifted into the canonical specs under the `SPMS-STD-ID` scheme (25 new
capability IDs across the seven targets; new owned entities and concrete attribute tables; promoted
specialized rules). Shared/schema-level detail was added to `SPMS-DOMAIN-MODEL` first (Level 2
controlled change): relationship registry entries `SPMS-TRACE-GRAPH-REL-016…020`
(`governed-by`, `hosted-on`, `connected-to`, `backed-up-by`, `monitored-by`); `TraceLink`
`rationale`/`confidence`/`validity_state`; `Approval` quorum/parallel/conditional + e-signature
metadata; an `EvidencePackage` schema and `AuditEvent` before/after summary; and the RBAC/ABAC
permission-inheritance and attribute model in §7.2. All 19 component specs still pass
`tools/spec_lint.py`. The corresponding specs remain v0.2 Draft; promotion to v1.0 still requires
named reviewer/approver sign-off per `SPMS-INDEX`.

Remaining open items (H-04, H-05, H-06 Medium; H-11, H-12, H-13 Low) are unchanged and are
expected to be harvested as their components enter detailed design per the Phase Implementation
Plan.
