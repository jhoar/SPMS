# SPMS Specification Set — Reconciled Set v1

This package is the reconciled, single-authoritative version of the SPMS specification corpus,
produced 2026-06-14. It implements the corrections and improvements agreed in review.

## What changed (corrections)

1. **One authoritative set.** The corpus previously held two overlapping families (a named set and
   a numbered set). They are reconciled into a single canonical set of **19 component
   specifications** in `specifications/`. The numbered set is superseded and archived read-only in
   `_superseded/`.
2. **The three "homeless" substrate concerns now have owners and specifications.** Baseline/version/
   change-control, the integration/event framework, and the physical persistence layer were
   promoted into `SPMS-BASE-CCB`, `SPMS-INT-EVENT`, and `SPMS-DATA-STORE`. Single ownership of every
   shared concern is recorded in `SPMS-DOMAIN-MODEL` §2.
3. **Global identifier scheme.** All capability identifiers are now globally unique and three-digit
   padded (`SPMS-<COMPONENT>-CAP-NNN`). Defined in `standards/SPMS-STD-ID`. Enforced by the linter.
4. **Authoritative source statement and register.** `programme/SPMS-INDEX` is the controlling
   register: the authoritative-source statement, the 19-spec list with owners and supersession, and
   the dependency overview. Every spec links back to it.
5. **Planning documents reconciled.** `standards/SPMS-METHODOLOGY` resolves the foundation-first vs
   vertical-slice contradiction; both planning documents were edited to point at it and to stop
   using "vertical slice" with two meanings.
6. **Scale envelope quantified.** `standards/SPMS-STD-SCALE` defines Small/Standard/Large profiles
   and binds the existing P95 targets to them, so the performance gates are now testable.
7. **Owners/reviewers/approvers assigned.** The TBD fields in every spec's Document Control are
   replaced with role-based owners, reviewers, and approvers.

## What was added (improvements)

- **Delivery plan and risk register** (`programme/SPMS-DELIVERY`): indicative effort, staffing, and
  timeline; a 10-item delivery-risk register; and the **thin governed thread** first increment that
  de-risks the foundation-first approach. The thread is also inserted as a milestone in the phase
  plan.
- **Specification linter** (`tools/spec_lint.py`): checks identifier format/uniqueness, required
  sections, reference resolution, NFR/scale binding, and TBD owners. Current result: **PASS**
  (19 specs, 158 unique capability IDs, 0 errors) — see `tools/lint_report.txt`. Wire it into CI.
- **Canonical domain model & relationship registry** (`standards/SPMS-DOMAIN-MODEL`): one record
  model, one lifecycle state set, one relationship-type registry, referenced by all specs so the
  corpus cannot silently re-diverge.

(The "dogfood the specs inside the tool" improvement was intentionally not implemented per request.)

## Layout

```
specifications/   19 canonical component specifications (authoritative)
standards/        SPMS-STD-ID, SPMS-STD-SCALE, SPMS-DOMAIN-MODEL, SPMS-METHODOLOGY
programme/        SPMS-INDEX (register), SPMS-DELIVERY, and the two edited planning documents
tools/            spec_lint.py, build_canonical.py, lint_report.txt
_superseded/      the 16 superseded numbered specs (read-only) + README
DETAIL-HARVEST-BACKLOG.md   net-new detail to lift from superseded specs during detailed design
```

## How to verify

```
python3 tools/spec_lint.py .
```

Start from `programme/SPMS-INDEX_specification-register.md`.
