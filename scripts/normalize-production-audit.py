from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "normalized-production-audit"
OUT.mkdir(parents=True, exist_ok=True)

# The original live audit predates the form-label and direct-404 corrections.
# Keep its rendered cells as evidence, but exclude only the two verified probe errors.
route_cells = json.loads((EVIDENCE / "exhaustive-live-audit" / "route-viewport-cells.json").read_text())
exhaustive = []
excluded = []
for cell in route_cells:
    for finding in cell.get("findings", []):
        record = {
            "source": "exhaustive-live-audit",
            "route": cell.get("route"),
            "viewport": cell.get("viewport", {}).get("label"),
            **finding,
        }
        if finding.get("code") == "nameless-interactive":
            excluded.append({**record, "reason": "Controls are associated with visible label elements; the old probe did not compute label-based accessible names."})
            continue
        if finding.get("code") == "unexpected-status" and cell.get("route") == "/404/" and finding.get("detail", {}).get("actual") == 200:
            excluded.append({**record, "reason": "The directly addressable 404 information page intentionally returns 200; unknown paths are separately required to return 404."})
            continue
        exhaustive.append(record)

supplemental_raw = json.loads((EVIDENCE / "post-deployment-audit" / "findings.json").read_text())
supplemental = []
for finding in supplemental_raw:
    if finding.get("code") == "unnamed-interactive-controls":
        excluded.append({"source": "post-deployment-audit", **finding, "reason": "Controls are associated with visible label elements; the old probe did not compute label-based accessible names."})
        continue
    if finding.get("code") == "unexpected-status" and finding.get("route") == "/404/" and finding.get("detail", {}).get("actual") == 200:
        excluded.append({"source": "post-deployment-audit", **finding, "reason": "The directly addressable 404 information page intentionally returns 200."})
        continue
    supplemental.append({"source": "post-deployment-audit", **finding})

quality = json.loads((EVIDENCE / "production-quality-audit" / "findings.json").read_text())
quality = [{"source": "production-quality-audit", **finding} for finding in quality]
findings = exhaustive + supplemental + quality
summary = {
    "findingCount": len(findings),
    "severityCounts": dict(Counter(item.get("severity", "unknown") for item in findings)),
    "findingCodes": dict(Counter(item.get("code", "unknown") for item in findings)),
    "excludedInstrumentationFindings": len(excluded),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
(OUT / "findings.json").write_text(json.dumps(findings, indent=2))
(OUT / "excluded-instrumentation-findings.json").write_text(json.dumps(excluded, indent=2))
print(json.dumps(summary, indent=2))
