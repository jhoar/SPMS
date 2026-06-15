#!/usr/bin/env python3
"""
Build the canonical SPMS specification set (reconciled set v1).

- Normalizes Document Control on the 16 named specs (real owners/reviewers/approvers,
  version bump, authoritative/supersedes/register rows, authority block).
- Promotes the 3 substrate concerns that had no named owner (baseline/version/change-control,
  integration/event framework, data persistence) by adapting SUB-006/008/009 into the
  canonical format and ID scheme.
Outputs to specifications/.
"""
import re, glob, os, datetime

SRC = "/home/claude/work"
OUT = "/home/claude/work/specifications"
os.makedirs(OUT, exist_ok=True)

TODAY = "2026-06-14"
REVIEWERS = "SPMS Architecture Review Board"
APPROVERS = "Engineering Director; Programme Technical Authority"

AUTHORITY_BLOCK = (
    "> **Authoritative specification — reconciled set v1 ({today}).**\n"
    "> This document is part of the single authoritative SPMS specification set. It supersedes the\n"
    "> superseded draft(s) listed in Document Control. For the controlling register, identifier rules,\n"
    "> canonical domain model, scale envelope, and delivery methodology, see: `SPMS-INDEX` (register),\n"
    "> `SPMS-DOMAIN-MODEL`, `SPMS-STD-ID`, `SPMS-STD-SCALE`, and `SPMS-METHODOLOGY`.\n"
    "> Where this document and any superseded draft differ, this document governs. Net-new detail in\n"
    "> superseded drafts is tracked in `DETAIL-HARVEST-BACKLOG` for incorporation during detailed design.\n\n"
).format(today=TODAY)

# code -> (glob, owner, supersedes, kind, display_name, new_title, new_filename)
NAMED = {
    "PLAT-CORE":        ("Platform Architecture Lead",   "SPMS-SUB-001; SPMS-SUB-002 (record-model portion); SPMS-SUB-010 (admin/ops portion)"),
    "WF-GOV":           ("Governance Engineering Lead",  "SPMS-SUB-003"),
    "TRACE-GRAPH":      ("Traceability & Data Lead",      "SPMS-SUB-004"),
    "EVID-AUDIT":       ("Assurance Data Lead",           "SPMS-SUB-005"),
    "WP-PLAN":          ("Delivery Modules Lead",         "—"),
    "ISS-CHG":          ("Delivery Modules Lead",         "—"),
    "REQ-MGMT":         ("Requirements & V&V Lead",       "—"),
    "DOC-KM":           ("Delivery Modules Lead",         "—"),
    "TEST-VV":          ("Requirements & V&V Lead",       "—"),
    "CICD":             ("Engineering Integration Lead",  "—"),
    "REL-DEP":          ("Release Engineering Lead",      "SPMS-FUN-011"),
    "CFG-ASSET":        ("Release Engineering Lead",      "SPMS-FUN-012"),
    "SEC-COMP":         ("Security & Compliance Lead",    "SPMS-FUN-013; SPMS-SUB-010 (security portion)"),
    "PROD-ASSUR":       ("Product Assurance Lead",        "SPMS-FUN-014"),
    "REPORT-ANALYTICS": ("Analytics Lead",                "SPMS-FUN-015; SPMS-SUB-007"),
    "AUTO-AI":          ("AI Assurance Lead",             "SPMS-FUN-016"),
}

# promoted: source SUB file -> new code, owner, display name, new title, filename
PROMOTED = {
    "SPMS-SUB-006": dict(code="BASE-CCB", owner="Assurance Data Lead",
        name="Baseline, Version & Change-Control Engine",
        title="# Baseline, Version & Change-Control Engine Specification",
        fname="SPMS-BASE-CCB_baseline-version-change-control_specification.md",
        ctype="Platform substrate"),
    "SPMS-SUB-008": dict(code="INT-EVENT", owner="Engineering Integration Lead",
        name="Integration & Event Framework",
        title="# Integration & Event Framework Specification",
        fname="SPMS-INT-EVENT_integration-event-framework_specification.md",
        ctype="Platform substrate"),
    "SPMS-SUB-009": dict(code="DATA-STORE", owner="Platform Architecture Lead",
        name="Data Persistence Layer (Object Storage, Relational DB, Graph Projection, Search Index, Metrics Store)",
        title="# Data Persistence Layer Specification",
        fname="SPMS-DATA-STORE_data-persistence-layer_specification.md",
        ctype="Platform substrate"),
}

def set_row(text, field, value):
    pat = re.compile(r'(?m)^\| %s \| .*\|\s*$' % re.escape(field))
    repl = '| %s | %s |' % (field, value)
    if pat.search(text):
        return pat.sub(lambda m: repl, text, count=1)
    return text

def insert_dc_rows(text, rows):
    # insert extra rows after the "Last updated" row
    marker = re.compile(r'(?m)^(\| Last updated \| .*\|\s*)$')
    add = "\n".join("| %s | %s |" % (k, v) for k, v in rows)
    return marker.sub(lambda m: m.group(1) + "\n" + add, text, count=1)

def insert_authority(text):
    # insert authority block immediately before "# 1. Purpose"
    return re.sub(r'(?m)^(# 1\. Purpose)', AUTHORITY_BLOCK + r'\1', text, count=1)

def normalize_named(text, code, owner, supersedes):
    text = set_row(text, "Version", "0.2")
    text = set_row(text, "Status", "Draft — Authoritative (reconciled set v1)")
    text = set_row(text, "Owner", owner)
    text = set_row(text, "Reviewers", REVIEWERS)
    text = set_row(text, "Approvers", APPROVERS)
    text = set_row(text, "Last updated", TODAY)
    text = insert_dc_rows(text, [
        ("Authoritative", "Yes"),
        ("Supersedes", supersedes),
        ("Specification register", "SPMS-INDEX"),
        ("Canonical domain model", "SPMS-DOMAIN-MODEL"),
        ("Identifier standard", "SPMS-STD-ID"),
    ])
    text = insert_authority(text)
    return text

def promote(text, cfg):
    code = cfg["code"]
    # title (first heading)
    text = re.sub(r'(?m)\A# .*', cfg["title"], text, count=1)
    # DC rows
    text = set_row(text, "Specification ID", "SPMS-%s" % code)
    text = set_row(text, "Component name", cfg["name"])
    text = set_row(text, "Component type", cfg["ctype"])
    text = set_row(text, "Version", "0.2")
    text = set_row(text, "Status", "Draft — Authoritative (reconciled set v1)")
    text = set_row(text, "Owner", cfg["owner"])
    text = set_row(text, "Reviewers", REVIEWERS)
    text = set_row(text, "Approvers", APPROVERS)
    text = set_row(text, "Last updated", TODAY)
    text = insert_dc_rows(text, [
        ("Authoritative", "Yes"),
        ("Supersedes", cfg["src"]),
        ("Specification register", "SPMS-INDEX"),
        ("Canonical domain model", "SPMS-DOMAIN-MODEL"),
        ("Identifier standard", "SPMS-STD-ID"),
    ])
    # convert local CAP-NN -> SPMS-<code>-CAP-0NN  (2 digit -> 3 digit, namespaced)
    text = re.sub(r'\bCAP-(\d{2})\b', lambda m: "SPMS-%s-CAP-0%s" % (code, m.group(1)), text)
    text = insert_authority(text)
    return text

written = []

# named
for path in glob.glob(os.path.join(SRC, "SPMS-*.md")):
    base = os.path.basename(path)
    m = re.match(r'(SPMS-[A-Z-]+)_', base)
    if not m:
        continue
    code = m.group(1).replace("SPMS-", "")
    if code in NAMED and not base.startswith("SPMS-SUB") and not base.startswith("SPMS-FUN"):
        owner, supersedes = NAMED[code]
        text = open(path, encoding="utf-8").read()
        text = normalize_named(text, code, owner, supersedes)
        open(os.path.join(OUT, base), "w", encoding="utf-8").write(text)
        written.append(base)

# promoted
for srcid, cfg in PROMOTED.items():
    cfg["src"] = srcid
    src_path = glob.glob(os.path.join(SRC, srcid + "_*.md"))[0]
    text = open(src_path, encoding="utf-8").read()
    text = promote(text, cfg)
    open(os.path.join(OUT, cfg["fname"]), "w", encoding="utf-8").write(text)
    written.append(cfg["fname"])

print("Canonical specs written: %d" % len(written))
for w in sorted(written):
    print("  ", w)
