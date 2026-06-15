# UI/UX Information Architecture

## 0. Document Control

| Field | Value |
|---|---|
| Specification ID | SPMS-UX |
| Component name | UI/UX Information Architecture |
| Component type | Programme document |
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
> For the controlling register and related standards, see: `SPMS-INDEX` (register),
> `SPMS-DOMAIN-MODEL`, `SPMS-STD-MODULE`, and `SPMS-METHODOLOGY`.

# 1. Purpose

Module specifications (`SPMS-WP-PLAN`, `SPMS-ISS-CHG`, `SPMS-REQ-MGMT`, etc.) each list their
module-specific screens and capabilities. This document defines the **shared structural shell**
in which all modules appear: the navigation model, workspace hierarchy, queue semantics, global
search experience, record detail layout, graph exploration UX, dashboard strategy, and admin
configuration UX.

Module specifications are authoritative for module-specific fields, record types, and workflows.
This document is authoritative for the cross-module shell. Where a module specification and this
document conflict on shared UI structure, this document governs.

# 2. Workspace Hierarchy

## 2.1 Logical hierarchy

```
Tenant
  └── Programme / Portfolio  (optional grouping, may be absent in Small profile)
        └── Product / Project
              └── Module  (Issues, Requirements, Documents, Tests, CI/CD, …)
                    └── Record
```

- **Tenant** — Top-level isolation boundary. A user belongs to one tenant per session.
- **Programme / Portfolio** — Optional grouping of multiple Products or Projects; not required
  in the Minimum Viable Governed Deployment (`SPMS-STD-SCALE` §5).
- **Product / Project** — The primary unit of work. A team works within one or more projects.
  A project has a governance profile, an enabled-module list, and an owner.
- **Module** — A functional capability (e.g., Requirements, Issues, CI/CD). Modules are enabled
  per project by the project administrator.
- **Record** — A single controlled item within a module (e.g., a requirement, an issue, a
  document). Records carry a globally unique SPMS id.

## 2.2 URL structure

URLs follow the pattern:

```
/<tenant-slug>/<project-slug>/<module>/<record-id>
```

Examples:
- `/acme/flight-software/requirements/SPMS-REQ-MGMT-00042`
- `/acme/flight-software/issues/SPMS-ISS-CHG-00017`
- `/acme/flight-software/graph` (cross-module traceability view)

## 2.3 Top-level shell

The persistent top-level navigation bar (present on every screen):

```
[ Tenant logo / switcher ]  [ Project selector ▾ ]  [ My Work (N) ]  [ 🔍 Search ]  [ 🔔 N ]  [ Avatar ▾ ]
```

- **Tenant logo / switcher** — Clickable; opens tenant list for multi-tenant users.
- **Project selector** — Dropdown of accessible projects in the current tenant; shows project
  name, module badge counts, governance profile.
- **My Work (N)** — Badge count of pending actions; opens the My Work queue (§4).
- **Search** — Opens the Global Search experience (§5).
- **Notification bell** — Count of unread notifications; opens notification panel.
- **Avatar** — User display name, settings, logout.

# 3. Navigation Model

## 3.1 Left sidebar (project context)

When a project is selected, a persistent left sidebar provides module navigation:

| Icon / label | Destination | Badge |
|---|---|---|
| Home | Project dashboard | — |
| My Work | Personal queue (§4) | Pending items count |
| Requirements | `SPMS-REQ-MGMT` list | Open requirements count |
| Issues | `SPMS-ISS-CHG` list | Open issues count |
| Documents | `SPMS-DOC-KM` list | Overdue reviews count |
| Tests | `SPMS-TEST-VV` list | Failed / open tests count |
| CI/CD | `SPMS-CICD` list | Failed builds count |
| Security | `SPMS-SEC-COMP` list | Open critical vulnerabilities count |
| Releases | `SPMS-REL-DEP` list | Pending releases count |
| Assets | `SPMS-CFG-ASSET` list | Drift alerts count |
| Traceability | Graph explorer (§7) | Suspect links count |
| Reports | `SPMS-REPORT-ANALYTICS` | — |
| AI Assist | `SPMS-AUTO-AI` | — |
| ⚙ Admin | Admin panel (§9) | — (role-gated) |

Modules that are not enabled for the project are hidden (not greyed out) to avoid confusion.
The sidebar is collapsible to an icon-only strip.

## 3.2 Breadcrumb

Every screen shows a breadcrumb immediately below the top navigation bar:

```
Acme Corp  ›  Flight Software  ›  Requirements  ›  SPMS-REQ-MGMT-00042 — Altitude Hold Requirement
```

Each segment is a clickable link to that level of the hierarchy.

# 4. Queue Semantics ("My Work")

## 4.1 Purpose

My Work is the **unified personal inbox** aggregating all actions the current user must take
across all modules in the current project. It is the default landing page for users logging in.

## 4.2 Content

| Item type | Description | Shown when |
|---|---|---|
| Pending approval | Record awaiting this user's approval | User is a required approver; record is in `in_review` or gate-pending state |
| Pending review | Record assigned to this user for review | User is an assigned reviewer |
| Overdue owned record | Record owned by this user with missed SLA or overdue date | SLA timer has expired or target date passed |
| Blocking gate | A gate this user must clear to allow downstream progression | User's approval is blocking a gate |
| Suspect link requiring action | A trace link marked suspect where this user owns the downstream record | Suspect flag is unresolved |
| AI proposal awaiting acceptance | An AI-generated draft assigned to this user for review | Proposal in staging state awaiting one-click acceptance |

## 4.3 Display

Each item in the queue shows:
- Record type icon | Record ID | Record title
- Action required (e.g., "Approve", "Review", "Clear gate", "Resolve suspect link")
- SLA countdown (amber when < 24 h remaining; red when overdue)
- Quick-action buttons: primary action (e.g., "Approve") + "Open record" link

## 4.4 Sorting and filtering

Default sort: SLA urgency (overdue first, then by time remaining). User may change to:
- Date created (oldest first)
- Record type (grouped)
- Module (grouped)

Filters: module, record type, action type, SLA status.

# 5. Global Search

## 5.1 Entry point

The search bar is accessible from any screen via the top navigation bar. Activation (click or
keyboard shortcut) opens a search overlay without navigating away from the current page.

## 5.2 Search scope

Default scope: current project. User may toggle to "All accessible projects" or "This module".

## 5.3 Supported query types

| Query type | Syntax | Example |
|---|---|---|
| Full-text | Natural language | `altitude hold` |
| Exact ID | Record ID | `SPMS-REQ-MGMT-00042` |
| Filter syntax | `field:value` | `type:requirement state:approved` |
| Combined | Filters + text | `type:issue owner:jane blocked` |

## 5.4 Result presentation

Results are grouped by record type:

```
Requirements (12)
  ● SPMS-REQ-MGMT-00042  Altitude Hold Requirement  [approved]  J. Smith  2 days ago
  ● SPMS-REQ-MGMT-00089  Rate Limiter Requirement   [in_review] T. Jones  5 hours ago
  ...
Issues (3)
  ● SPMS-ISS-CHG-00017  Altitude drift after mode switch  [open]  A. Patel  1 hour ago
  ...
```

Result cards show: ID, title, state badge, owner, last updated. Clicking opens the record
detail view.

## 5.5 Permission filter

Search results are permission-filtered: the search index returns only records the current user
can read (`SPMS-STD-SEC` §3). Restricted-classification records are returned only if the user
has sufficient clearance; their titles are visible but sensitive field content is redacted in
the result card.

## 5.6 Recent and suggested searches

The search overlay shows recent searches and suggested record IDs from the user's browsing
history (stored client-side only; not persisted to the server).

# 6. Record Detail Layout

## 6.1 Consistent shell

Every record type (requirement, issue, document, test case, asset, vulnerability, etc.) uses
the same structural shell. Module-specific fields appear within the Details tab.

```
┌──────────────────────────────────────────────────────────────────────┐
│  SPMS-REQ-MGMT-00042 │ Altitude Hold Requirement │ [approved] │ 🔒 internal │
│  Owner: J. Smith │ Project: Flight Software │ Baseline: FB-v2.1       │
│  [Submit] [Approve] [Add to Baseline ▾] [Link ▾] [Export ▾] [⋯]   │
├──────────────────────────────────────────────────────────────────────┤
│  Details │ Links & Traceability │ Evidence │ History │ Activity      │
├──────────────────────────────────────────────────────────────────────┤
│  (tab content — see §6.2–§6.6)                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## 6.2 Header strip

| Element | Description |
|---|---|
| Record ID | Globally unique; copyable to clipboard on click |
| Title | Editable inline (gated by `edit` permission and workflow state) |
| State badge | Colour-coded lifecycle state; tooltip shows allowed transitions |
| Classification badge | Shows classification level; locked icon for `confidential` or `restricted` |
| Owner | Clickable user name; tooltip shows team and contact |
| Baseline membership | Shows current baseline(s) the current version participates in |
| Actions dropdown | Context-sensitive: shows only permitted transitions/actions for current state and user role |

## 6.3 Details tab

- Two-column form layout for record-type-specific fields.
- Read-only by default; "Edit" button (top-right of tab) enables inline editing.
- "Edit" is gated by permission and workflow state (e.g., fields are locked in `approved`
  state without a change request).
- Mandatory fields highlighted in a distinct colour when empty.

## 6.4 Links & Traceability tab

- Outgoing and incoming trace links grouped by link type (§5 of `SPMS-DOMAIN-MODEL`).
- Each link row: linked record ID + title + state + link type + "suspect" amber badge if
  flagged.
- "Add link" button opens the linked-record picker (`SPMS-STD-MODULE` §4).
- "Expand to Graph" button opens the Graph Explorer (§7) centred on this record.
- Mini graph thumbnail (up to 1-hop neighbourhood) rendered inline.

## 6.5 Evidence tab

- List of attached evidence records: type icon, title, uploaded-by, date, status badge.
- Expired evidence shown with amber warning; revoked with red.
- "Attach evidence" button opens the evidence upload dialog.
- Evidence file preview (where format allows: PDF, image, text).

## 6.6 History tab

- Version table: version number, changed-by, changed-at (timestamp), diff summary (fields
  changed with old → new values).
- "View at version N" button opens a read-only historical snapshot of the record at that
  version (calls historical reconstruction via `SPMS-TRACE-GRAPH` / `SPMS-BASE-CCB`).
- "Compare versions" allows selecting two version rows to show a side-by-side diff.

## 6.7 Activity tab

- Chronological feed of all events on this record: comments, state changes, approval decisions,
  evidence actions, link changes, export events, AI actions.
- Each entry: actor avatar + name, action description, timestamp.
- Comment box at the bottom (gated by `comment` permission).
- @mention support for users in the project.

# 7. Graph Exploration UX

## 7.1 Access points

The Graph Explorer is accessible from:
- The **Links & Traceability tab** "Expand to Graph" button (opens centred on the current record).
- The **Traceability** module in the left sidebar (opens with project-level overview).
- A direct URL: `/<tenant>/<project>/graph?focus=<record-id>`.

## 7.2 Canvas

- **Force-directed layout** by default; toggleable to hierarchical (top-down) or radial.
- **Node appearance:** Coloured by record type (each module type has a distinct colour);
  shape indicates state (filled = approved/baselined, outline = draft/in_review).
- **Edge appearance:** Line style by link type; direction indicated by arrowhead.
- **Suspect links:** Highlighted in amber with a warning icon on the edge.
- **Coverage gaps:** Records with no incoming `verifies` link shown with a red border (optional,
  configurable per project).

## 7.3 Controls

| Control | Description |
|---|---|
| Depth slider (1–5) | Limits traversal depth from the focal node(s) |
| Record type filter | Show/hide node types (e.g., show only Requirements and Tests) |
| Link type filter | Show/hide edge types (e.g., show only `verifies` and `implements`) |
| Highlight suspect | Toggle amber highlighting for suspect links |
| Highlight coverage gaps | Toggle red border for uncovered requirements |
| Search in graph | Find and focus on a record within the current graph view |
| Layout toggle | Force-directed / Hierarchical / Radial |
| Zoom / pan | Standard canvas zoom; fit-to-view button |

## 7.4 Historical mode (Historical Graph Explorer)

The "View at baseline/date" selector invokes the Historical Graph Explorer
(`SPMS-TRACE-GRAPH` CAP-008):

1. User selects a named baseline from a dropdown or enters a date/time.
2. The canvas re-renders showing the graph topology, node states, link types, and evidence
   status as they existed at that point in time.
3. A persistent mode banner indicates "Viewing graph at: <baseline name / date>" with an
   "Exit historical view" button.
4. Historical mode is read-only; no mutations are possible while in this mode.
5. Historical mode does not affect the live graph; it is a separate view of the
   point-in-time snapshot.

## 7.5 Node interaction

- **Single click:** Opens a record summary panel on the right side of the canvas (title, state,
  owner, classification, recent activity) without leaving the graph.
- **Double click / "Open record" button in panel:** Navigates to the full record detail view.
- **Right-click context menu:** Add link from this node; navigate to record; show/hide
  neighbourhood; pin node.

# 8. Dashboard Strategy

## 8.1 Dashboard hierarchy

| Level | Scope | Default occupant |
|---|---|---|
| Project dashboard | Single project | Landing page when a project is selected |
| Tenant dashboard | All accessible projects | Landing page for tenant administrators |
| Personal dashboard | My Work and assigned items | Accessible from avatar menu; optional |
| Module dashboard | Single module within a project | Accessible from module in sidebar |

## 8.2 Default role-based dashboards

Each project dashboard shows a role-appropriate default view on first access:

| Role | Default widgets |
|---|---|
| Product Owner / Project Manager | Scope coverage (% requirements linked to tests), velocity (issues closed/week), open blockers, release readiness gate status |
| Technical Lead | Build health (pass rate, last failure), open blockers by module, test coverage trend, recent deployments |
| Auditor / QA | Evidence completeness by gate, baseline age, overdue reviews, gate status heatmap |
| Security Lead | Open vulnerabilities by severity (funnel), compliance posture (control coverage %), exception expiry timeline |
| Automation / AI Lead | AI proposal acceptance rate, Grounding Attestation completeness, automation rule execution health |

## 8.3 Composable widgets

All dashboards are composable: users drag, drop, add, and remove widgets. Widget settings
(filters, time ranges, groupings) are saved per user per dashboard.

Widget library:

| Widget type | Description |
|---|---|
| Status funnel | Count of records by lifecycle state; filterable by type, owner, module |
| Aging chart | Record count by age bucket (< 7 d, 7–30 d, > 30 d); configurable buckets |
| Coverage matrix | Rows: source record type; columns: target record type; cells: % with qualifying link |
| Trend line | Metric over time (e.g., open issues, failed builds, coverage %) |
| Heat map | Two-dimensional grid (e.g., severity × age for vulnerabilities) |
| Table view | Configurable columns; sorts and filters; links to records |
| Metric counter | Single prominent number with delta and trend arrow |
| SLA tracker | Records approaching or past SLA deadline; colour-coded urgency |
| Gate status | Gate-by-gate readiness indicator for a release; green/amber/red |

## 8.4 Drill-through

Every widget data point is clickable and navigates to a filtered record list showing the
underlying records. The filter applied by the drill-through is visible in the record list view.

# 9. Admin Configuration UX

## 9.1 Access

The Admin panel is accessible from the ⚙ Admin icon in the left sidebar. It is visible only to
users with Tenant Administrator or Project Administrator roles. Tenant-level settings require
the Tenant Administrator role; project-level settings require at minimum Project Administrator.

## 9.2 Admin sections

| Section | Scope | Key capabilities |
|---|---|---|
| Tenant Settings | Tenant | Name, branding (logo, colours), SSO/OIDC configuration, secret manager reference, default governance profile, retention policies |
| Project Settings | Project | Project name, governance profile override, enabled modules, team/role assignment, project-level retention policy, archive/suspend |
| Workflow Designer | Project | Visual state-machine editor per record type; add/remove states, transitions, triggers, conditions, required approvals, automatic actions; activate / deprecate workflow definitions |
| Schema Editor | Project | Add/remove/reorder fields on record types; set required/optional; configure validation rules (regex, range, enum); configure field-level classification |
| Integration Manager | Tenant / Project | Add and configure integration connectors (Git, CI/CD, scanner, CMDB, SBOM, etc.); view sync status and last-run result; access dead-letter queue for review and replay; configure re-sync schedule |
| Governance Profiles | Project | Configure Low-risk bulk profile whitelist (which record types and fields are eligible); configure approval rules and quorum for each profile level; configure gate thresholds |
| Retention Policies | Tenant | Set retention class durations (standard, long, permanent); configure WORM policy; set evidence expiry review schedule |
| AI Configuration | Tenant / Project | Select AI model (references `SPMS-AUTO-AI`); configure grounding scope (which record types and classifications may be retrieved); set classification permission boundary; schedule red-team evaluation; configure Grounding Attestation requirements |
| Audit & Compliance | Tenant | View and validate hash chain integrity; trigger audit log export; schedule compliance export packages; view tamper-resistance check history |

## 9.3 Governance of admin actions

All admin panel actions are **Level 2 or Level 3 governance changes** per `SPMS-METHODOLOGY`
and the agile validation approach:
- Workflow definition changes: Level 2 (design note required; contract tests for transitions).
- Schema changes affecting existing data: Level 2 or Level 3 depending on whether the change
  is reversible and affects `restricted` data.
- SSO/identity configuration changes: Level 3 (two-person review; security review).
- Retention policy changes: Level 3 (irreversible if retention is shortened; data destruction
  risk).
- AI configuration changes (model, scope, classification boundary): Level 2 with security
  review.

Every admin panel action must produce an `AuditEvent` record (`SPMS-STD-SEC` §7; `SPMS-STD-MODULE` §6).

## 9.4 Preview and dry-run in admin

Where an admin action affects existing records or workflows:
- **Workflow Designer:** Activating a new workflow definition shows a preview of affected
  in-flight records and required migration steps (records in states that no longer exist must
  be migrated to the nearest valid state or held in a `suspended` side state).
- **Schema Editor:** Adding a required field shows a count of existing records that will fail
  the new validation; a back-fill script must be configured before activation.
- **Governance Profile changes:** Changing from Controlled to Standard shows a list of records
  whose approval requirements will be affected; operator must confirm.
