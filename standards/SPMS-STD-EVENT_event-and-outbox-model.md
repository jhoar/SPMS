# Event & Outbox Model Standard

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-STD-EVENT |
| Component name | Event & Outbox Model Standard |
| Component type | Programme standard (normative) |
| Version | 0.1 |
| Status | Draft — Authoritative (reconciled set v1) |
| Owner | Engineering Integration Lead |
| Reviewers | SPMS Architecture Review Board |
| Approvers | Engineering Director; Programme Technical Authority |
| Date created | 2026-06-15 |
| Last updated | 2026-06-15 |
| Applies to | Every component that mutates controlled records or consumes events |

---

> **Authoritative specification — reconciled set v1 (2026-06-14).**
> This document is part of the single authoritative SPMS specification set.
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.

# 1. Purpose and Scope

This standard defines the mandatory event and outbox model for all SPMS components. Every
controlled mutation must apply the transactional outbox pattern so that derived projections
(graph, search, reporting) are always consistent with the relational record store and can be
rebuilt without data loss.

This standard governs:
- Transactional outbox mechanics
- Event envelope schema (references `SPMS-DOMAIN-MODEL` §7.7)
- Projection consumption contract
- Idempotency requirements
- Retry and dead-letter semantics
- Projection rebuild protocol

Out of scope: event taxonomy (governed by `SPMS-INT-EVENT`), storage layer (governed by
`SPMS-DATA-STORE`), audit log tamper resistance (governed by `SPMS-STD-SEC`).

# 2. Transactional Outbox Pattern

## 2.1 Mandatory write rule

Every controlled mutation (record create, update, state change, approval, evidence attachment,
baseline operation, link creation) must write to **both** of the following in a single database
transaction:

1. The authoritative relational store (the record or entity being changed).
2. The `outbox` table — one row per domain event produced by the mutation, using the
   `IntegrationEvent` schema (`SPMS-DOMAIN-MODEL` §7.7).

If the transaction is rolled back, neither the record change nor the outbox row is committed.
There is no dual-write across a network boundary in the hot path.

## 2.2 Outbox relay process

A dedicated relay process (separate from the application request path) polls or tails the
outbox table for rows with `status = pending` and publishes them to the event bus:

1. Read a batch of `pending` rows ordered by `occurred_at` ascending within each tenant.
2. Publish each event to the event bus.
3. On confirmed acknowledgement from the bus, mark the row `status = published` and set
   `published_at`.
4. On failure after retries (§6), mark the row `status = dead-letter`.

The relay must run with at-least-once delivery semantics. Consumers handle deduplication via
the idempotency contract in §5.

## 2.3 Consumers must not read from the relational store for projection updates

Graph projection (`SPMS-TRACE-GRAPH`), search index (`SPMS-DATA-STORE`), and metrics/reporting
(`SPMS-REPORT-ANALYTICS`) must derive their state exclusively from the event stream, not from
direct reads of the relational record tables. This ensures projections are independently
rebuildable and that the relational store is not a shared-read bottleneck for derived views.

# 3. Event Envelope Schema

The envelope schema is the `IntegrationEvent` entity defined in `SPMS-DOMAIN-MODEL` §7.7.
Every event on the bus must conform to that schema. The `payload` field is event-type-specific
and its schema is versioned independently via `schema_version`.

## 3.1 Mandatory envelope fields

| Field | Rule |
|---|---|
| `event_id` | UUID v4; immutable; globally unique; used as deduplication key by all consumers |
| `tenant_id` | Must match the tenant of the mutated aggregate; consumers must reject cross-tenant events |
| `aggregate_id` | Id of the mutated record or entity |
| `aggregate_type` | Record type or entity name; consumers filter by this field |
| `event_type` | Registered type from `SPMS-INT-EVENT` event taxonomy |
| `schema_version` | Semantic version string of the `payload` schema; consumers must reject unknown versions |
| `occurred_at` | ISO 8601 with microsecond precision; immutable; time of the originating mutation |
| `actor_id` | Id of the user or service that caused the mutation |

## 3.2 Payload versioning

Each `event_type` has an independently versioned payload schema. Schema changes follow semantic
versioning: breaking changes increment the major version; additive changes increment the minor
version. Consumers must handle minor-version additions gracefully (unknown fields ignored) and
must reject unknown major versions.

# 4. Projection Consumption Contract

## 4.1 Consumer checkpoint

Each projection consumer maintains a durable `checkpoint` record: the `event_id` of the last
successfully processed event for each tenant. On restart, the consumer resumes from the
checkpoint — it does not reprocess already-applied events (subject to the idempotency rule
in §5).

## 4.2 Ordering

Events are processed in `occurred_at` order within a tenant. Cross-tenant ordering is not
guaranteed and is not required (tenants are fully isolated).

## 4.3 Projection types and owners

| Projection | Owner component | Feeds |
|---|---|---|
| Graph projection | `SPMS-TRACE-GRAPH` | Impact analysis, coverage, suspect links, Historical Graph Explorer |
| Search index | `SPMS-DATA-STORE` | Global search, filtered list views |
| Metrics / aggregate store | `SPMS-REPORT-ANALYTICS` | Dashboards, trend reports, SLA metrics |
| Semantic / vector index | `SPMS-DATA-STORE` | AI retrieval, duplicate detection |

## 4.4 Eventual consistency

Projections are eventually consistent with the relational store. The maximum acceptable lag is
bounded by `NFR-PERF-006` (P95 < 60 s end-to-end event processing, `SPMS-STD-SCALE` §3).
UI components that display projection-derived data must indicate recency where lag matters
(e.g., "as of <timestamp>").

# 5. Idempotency Requirements

## 5.1 Deduplication key

`event_id` is the deduplication key. Every consumer must check whether `event_id` has already
been applied before processing. A processed-event log (keyed by `consumer_id` + `event_id`) must
be maintained durably.

## 5.2 Idempotent handlers

Every event handler must produce the same result when applied one or more times. Handlers must
not use side effects that are not idempotent (e.g., incrementing a counter without a guard,
sending a notification more than once).

# 6. Retry and Dead-Letter Semantics

## 6.1 Retry policy

On delivery or processing failure, the relay or consumer applies exponential backoff:
- Attempt 1: immediate
- Attempt 2: 2 s delay
- Attempt 3: 8 s delay
- Attempt 4+: configurable (default maximum 5 attempts; maximum delay 60 s)

## 6.2 Dead-letter handling

After the maximum retry count, the event is moved to the dead-letter queue and the outbox row
(or consumer offset) is marked `dead-letter`. The following actions are taken automatically:
- A monitoring alert is raised for operator review.
- The event remains in the dead-letter queue for at least the tenant's audit retention period.
- Operators may manually replay or discard dead-letter events after root-cause investigation.
- Discard of a dead-letter event must produce an `AuditEvent` of type `DeadLetterDiscarded`.

# 7. Projection Rebuild Protocol

## 7.1 Full rebuild

A full rebuild replays all events for a tenant from the beginning of the `AuditEvent` log:

1. Spin up an empty projection store (graph DB, search index, metrics store).
2. Replay all `AuditEvent` records for the tenant in `occurred_at` order, applying each to the
   empty projection.
3. Validate the rebuilt projection (§7.3).
4. Swap the live projection for the rebuilt one atomically (blue/green swap).
5. Decommission the old projection store.

A full rebuild must not require service downtime.

## 7.2 Incremental rebuild

An incremental rebuild applies events since the last checkpoint:

1. Identify the last-processed `event_id` from the consumer checkpoint.
2. Replay subsequent events in `occurred_at` order.
3. Update the checkpoint on success.

## 7.3 Rebuild validation

After any rebuild, validation must confirm:
- Record count in the projection matches the relational store for the tenant.
- A random sample (minimum 1% or 1,000 records, whichever is smaller) matches between
  projection and relational store on key fields.
- Any discrepancy is reported as a rebuild failure; the old projection is not decommissioned
  until validation passes.

## 7.4 Operational trigger

Rebuild must be triggerable by an authorised operator without code deployment, via an
administrative API or CLI command. The trigger and outcome must produce `AuditEvent` records
(`ProjectionRebuildStarted`, `ProjectionRebuildCompleted`, `ProjectionRebuildFailed`).

# 8. Cross-References

| Standard / Spec | Relationship |
|---|---|
| `SPMS-DOMAIN-MODEL` §7.4 | `AuditEvent` schema (append-only source of truth for replay) |
| `SPMS-DOMAIN-MODEL` §7.7 | `IntegrationEvent` schema (outbox envelope) |
| `SPMS-INT-EVENT` | Event taxonomy; registered event types; connector contracts |
| `SPMS-DATA-STORE` | Relational store, outbox table storage, projection stores, rebuild tooling |
| `SPMS-TRACE-GRAPH` | Graph projection consumer |
| `SPMS-REPORT-ANALYTICS` | Metrics and dashboard projection consumer |
| `SPMS-STD-SEC` §7 | Audit log tamper resistance (hash chain on `AuditEvent`) |
| `SPMS-STD-SCALE` | `NFR-PERF-006` (P95 < 60 s event processing) bounds projection lag |
