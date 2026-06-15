# Identifier & Naming Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-ID |
| Component name | Identifier & Naming Standard |
| Component type | Programme standard |
| Version | 1.0 |
| Status | Approved for reconciled set v1 |
| Owner | Platform Architecture Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-14 |
| Last updated | 2026-06-14 |
| Applies to | All SPMS specifications and all records created by the implemented system |

---

# 1. Purpose

Before reconciliation the specification corpus had no global identifier namespace. Capability
identifiers restarted inside every document (`CAP-003` meant a different thing in sixteen files)
and two encodings were in use (`SPMS-REL-DEP-CAP-001` in the named set, `CAP-01` in the numbered
set). For a platform whose central value is traceability, the specifications themselves could not
be trace-linked. This standard defines a single identifier scheme used by every specification and,
forward, by every controlled record the system manages.

# 2. Specification identifiers

Each specification has a stable component code. The component code is uppercase, hyphen-separated,
and unique across the corpus.

| Component code | Specification |
|---|---|
| `SPMS-PLAT-CORE` | Platform Core |
| `SPMS-WF-GOV` | Workflow & Governance Core |
| `SPMS-TRACE-GRAPH` | Traceability Graph Core |
| `SPMS-EVID-AUDIT` | Evidence & Audit Core |
| `SPMS-BASE-CCB` | Baseline, Version & Change-Control Engine |
| `SPMS-INT-EVENT` | Integration & Event Framework |
| `SPMS-DATA-STORE` | Data Persistence Layer |
| `SPMS-WP-PLAN` | Planning & Work Packages |
| `SPMS-ISS-CHG` | Issue & Change Management |
| `SPMS-REQ-MGMT` | Requirements Management |
| `SPMS-DOC-KM` | Document & Knowledge Management |
| `SPMS-TEST-VV` | Test/V&V Management |
| `SPMS-CICD` | Build & CI/CD Management |
| `SPMS-REL-DEP` | Release & Deployment Management |
| `SPMS-CFG-ASSET` | Configuration & Asset Management |
| `SPMS-SEC-COMP` | Security & Compliance Management |
| `SPMS-PROD-ASSUR` | Product Assurance |
| `SPMS-REPORT-ANALYTICS` | Reporting & Analytics |
| `SPMS-AUTO-AI` | Automation & AI Assistance |

Programme standards and registers use their own codes: `SPMS-INDEX`, `SPMS-STD-ID`,
`SPMS-STD-SCALE`, `SPMS-DOMAIN-MODEL`, `SPMS-METHODOLOGY`, `SPMS-DELIVERY`.

# 3. Capability and requirement identifiers

Within a specification, identifiers follow this grammar:

```
SPMS-<COMPONENT>-<TYPE>-<NNN>
```

- `<COMPONENT>` is the component code from section 2 (without the leading `SPMS-`).
- `<TYPE>` is one of `CAP` (capability), `REQ` (requirement), `ENT` (data entity),
  `EVT` (domain event), `GATE` (governance gate), `NFR` (non-functional requirement).
- `<NNN>` is a zero-padded sequence, minimum three digits, never reused once retired.

Examples: `SPMS-REL-DEP-CAP-001`, `SPMS-BASE-CCB-CAP-010`, `SPMS-REQ-MGMT-NFR-004`.

Rules:

1. Identifiers are globally unique. The same `<TYPE>-<NNN>` may appear in two components only
   because the component code disambiguates them.
2. Padding is fixed at three digits across the whole corpus. `CAP-01` and `CAP-1` are invalid.
3. Identifiers are immutable. A capability that is dropped is marked retired in the register; its
   number is never re-issued.
4. Trace links cite full identifiers only. A bare `CAP-003` is invalid in any link, matrix, or
   coverage rule.

# 4. Runtime record identifiers

Records created by the running system (requirements, issues, tests, releases, evidence, etc.) use:

```
SPMS-<COMPONENT>-<TYPE>-<tenant-scoped sequence>
```

where the sequence is allocated per tenant by the Common Record Model (`SPMS-PLAT-CORE`). Record
identifiers are stable for the life of the record and survive supersession, baselining, and
archival. Historical reconstruction (`SPMS-BASE-CCB`, `SPMS-EVID-AUDIT`) resolves identifiers as of
a point in time.

# 5. Conformance

The specification linter (`tools/spec_lint.py`) enforces sections 2–3 mechanically: identifier
pattern, three-digit padding, global uniqueness, and link resolution. A specification that fails
these checks is not eligible to leave Draft status.
