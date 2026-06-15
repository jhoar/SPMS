#!/usr/bin/env python3
"""
SPMS specification linter.

Enforces the reconciled-set rules mechanically:
  - identifier pattern and three-digit padding (SPMS-STD-ID)
  - global uniqueness of capability identifiers
  - no unqualified local identifiers (bare CAP-NN)
  - cross-references resolve to a known component/standard (or documented legacy supersession)
  - required structural sections present in component specs
  - at least one numeric NFR target or a reference to the scale envelope
  - no TBD owner/approver left in Document Control
  - reconciled-set authority block present in component specs

Exit code 0 = clean (warnings allowed), 1 = at least one ERROR.
Usage: python3 spec_lint.py [root]   (default root = directory containing this script's repo)
"""
import re, os, sys, glob, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_DIR = os.path.join(ROOT, "specifications")
STD_DIRS = [os.path.join(ROOT, "standards"), os.path.join(ROOT, "programme")]

COMPONENT_CODES = [
    "SPMS-PLAT-CORE","SPMS-WF-GOV","SPMS-TRACE-GRAPH","SPMS-EVID-AUDIT","SPMS-BASE-CCB",
    "SPMS-INT-EVENT","SPMS-DATA-STORE","SPMS-WP-PLAN","SPMS-ISS-CHG","SPMS-REQ-MGMT",
    "SPMS-DOC-KM","SPMS-TEST-VV","SPMS-CICD","SPMS-REL-DEP","SPMS-CFG-ASSET","SPMS-SEC-COMP",
    "SPMS-PROD-ASSUR","SPMS-REPORT-ANALYTICS","SPMS-AUTO-AI",
]
STANDARD_CODES = ["SPMS-INDEX","SPMS-STD-ID","SPMS-STD-SCALE","SPMS-DOMAIN-MODEL",
                  "SPMS-METHODOLOGY","SPMS-DELIVERY",
                  "SPMS-STD-EVENT","SPMS-STD-SEC","SPMS-STD-MIG","SPMS-STD-MODULE",
                  "SPMS-THINTHREAD","SPMS-UX"]
KNOWN = sorted(COMPONENT_CODES + STANDARD_CODES, key=len, reverse=True)

REQUIRED_SECTIONS = [
    "Document Control", "Purpose and Scope", "Functional Capabilities",
    "Data Model", "Traceability and Impact Analysis",
    "Governance, Approvals, Waivers, and Gates",
    "Evidence, Audit, and Historical Reconstruction",
]

errors, warnings = [], []
def err(f, m): errors.append((f, m))
def warn(f, m): warnings.append((f, m))

def resolves(token):
    if re.match(r'^SPMS-(SUB|FUN)-\d+$', token):  # documented legacy supersession refs
        return True
    for c in KNOWN:
        if token == c or token.startswith(c + "-"):
            return True
    return False

cap_index = collections.defaultdict(list)   # cap id -> [files]

def lint_component(path):
    name = os.path.basename(path)
    text = open(path, encoding="utf-8").read()

    # sections
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            err(name, "missing required section: %s" % sec)

    # authority block
    if "reconciled set v1" not in text:
        err(name, "missing reconciled-set authority block")

    # owner / approver TBD
    for field in ("Owner", "Approvers"):
        m = re.search(r'(?m)^\| %s \| (.+?) \|\s*$' % field, text)
        if m and "TBD" in m.group(1):
            err(name, "%s still TBD in Document Control" % field)

    # unqualified local capability ids (CAP-NN not preceded by component code)
    for m in re.finditer(r'(?<![A-Z0-9-])CAP-\d{1,2}\b', text):
        err(name, "unqualified local identifier '%s' (use SPMS-<CODE>-CAP-NNN)" % m.group(0))

    # capability id pattern + padding + uniqueness
    for m in re.finditer(r'\bSPMS-[A-Z-]+-CAP-(\d+)\b', text):
        cid = m.group(0)
        if len(m.group(1)) < 3:
            err(name, "identifier not 3-digit padded: %s" % cid)
        cap_index[cid].append(name)

    # cross-reference resolution
    for m in re.finditer(r'\bSPMS-[A-Z0-9]+(?:-[A-Z0-9]+)*\b', text):
        tok = m.group(0)
        # ignore pure id-suffix tokens already validated; only check component-level prefix exists
        if not resolves(tok):
            warn(name, "unresolved reference: %s" % tok)

    # NFR numeric target or scale-envelope reference
    has_num = re.search(r'P9[59]|[0-9]+\s*(s|sec|seconds|ms|%|TB|records/hour|/day)', text)
    if not (has_num or "SPMS-STD-SCALE" in text):
        err(name, "no numeric NFR target and no reference to SPMS-STD-SCALE")

def lint_standard(path):
    name = os.path.basename(path)
    text = open(path, encoding="utf-8").read()
    if "## 0. Document Control" not in text:
        err(name, "missing Document Control")
    m = re.search(r'(?m)^\| Owner \| (.+?) \|\s*$', text)
    if m and "TBD" in m.group(1):
        err(name, "Owner still TBD")
    for mm in re.finditer(r'\bSPMS-[A-Z0-9]+(?:-[A-Z0-9]+)*\b', text):
        if not resolves(mm.group(0)):
            warn(name, "unresolved reference: %s" % mm.group(0))

comp_files = sorted(glob.glob(os.path.join(SPEC_DIR, "SPMS-*.md")))
for p in comp_files:
    lint_component(p)
for d in STD_DIRS:
    for p in sorted(glob.glob(os.path.join(d, "SPMS-*.md"))):
        lint_standard(p)

# global capability uniqueness: a cap id may recur within its own file (summary + detail),
# but must not appear in more than one distinct file.
dupes = {k: sorted(set(v)) for k, v in cap_index.items() if len(set(v)) > 1}
for cid, files in sorted(dupes.items()):
    err("(global)", "capability id %s appears in multiple files: %s" % (cid, ", ".join(files)))

print("=" * 70)
print("SPMS specification linter")
print("Component specs checked : %d" % len(comp_files))
print("Distinct capability IDs : %d" % len(cap_index))
print("Errors                  : %d" % len(errors))
print("Warnings                : %d" % len(warnings))
print("=" * 70)
for f, m in errors:
    print("ERROR  %-55s %s" % (f, m))
# collapse identical warnings for readability
wc = collections.Counter("%s :: %s" % (f, m) for f, m in warnings)
for k, n in sorted(wc.items()):
    print("WARN   %s%s" % (k, (" (x%d)" % n) if n > 1 else ""))
print("=" * 70)
print("RESULT:", "FAIL" if errors else "PASS")
sys.exit(1 if errors else 0)
