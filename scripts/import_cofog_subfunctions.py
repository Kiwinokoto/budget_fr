#!/usr/bin/env python3
"""Import second-level COFOG functions, 1995–2024, from the pinned Insee 3.301 XLSX."""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import urllib.request

if __package__:
    from .import_cofog import _grid, CODES, SOURCE_URL, SOURCE_SHA256, TOTAL_LABEL
else:
    from import_cofog import _grid, CODES, SOURCE_URL, SOURCE_SHA256, TOTAL_LABEL

OUTPUT = Path(__file__).resolve().parents[1] / "data/cofog_subfunctions_1995_2024.json"
CODE = re.compile(r"GF[0-9]{2}(?:[0-9]{2})?\Z")
LABEL = re.compile(r"^\s*[0-9]{1,2}\.[0-9]{1,2}\s+-\s+(.+)$")


def extract_subfunctions(blob):
    grid = _grid(blob)
    columns = [(int(raw), col) for col, raw in sorted(grid.get(4, {}).items())
               if col > 3 and str(raw or "").strip()]
    if [year for year, _ in columns] != list(range(1995, 2025)):
        raise ValueError("Unexpected COFOG years")
    series = {}
    for row in grid.values():
        code = row.get(2, "")
        if (row.get(0) == "OTE" and row.get(1) == TOTAL_LABEL and
                CODE.fullmatch(code)):
            if code in series:
                raise ValueError("Duplicate COFOG code: " + code)
            series[code] = row
    parents = list(CODES[1:])
    if not all(parent in series for parent in parents):
        raise ValueError("Missing COFOG parent")
    if any(code not in parents and not any(re.fullmatch(p + r"[0-9]{2}", code) for p in parents)
           for code in series):
        raise ValueError("Unexpected COFOG hierarchy")
    def amounts(row):
        values = []
        for _, col in columns:
            try:
                value = Decimal(str(row[col]))
            except (KeyError, InvalidOperation) as exc:
                raise ValueError("Missing/invalid COFOG figure") from exc
            if not value.is_finite() or value < 0:
                raise ValueError("Negative/nonfinite COFOG figure")
            values.append(value)
        return values
    categories = []
    for parent in parents:
        source_rows = [(code, row) for code, row in sorted(series.items())
                       if re.fullmatch(parent + r"[0-9]{2}", code)]
        if not source_rows:
            raise ValueError("COFOG parent without subfunctions: " + parent)
        children, sums = [], [Decimal(0)] * len(columns)
        for code, row in source_rows:
            match = LABEL.fullmatch(str(row.get(3, "")))
            if match is None:
                raise ValueError("Unknown source label format: " + code)
            values = amounts(row)
            sums = [a + b for a, b in zip(sums, values)]
            children.append({
                "code": code.lower(),
                "label": match.group(1).strip(),
                "values": [float(value) for value in values],
            })
        parent_values = amounts(series[parent])
        if any(abs(total - reported) > Decimal("0.015")
               for total, reported in zip(sums, parent_values)):
            raise ValueError("COFOG subdivisions do not reconcile: " + parent)
        categories.append({"code": parent.lower(), "children": children})
    if sum(len(item["children"]) for item in categories) != 69:
        raise ValueError("Unexpected number of second-level COFOG functions")
    return {"schema_version": 1, "years": [year for year, _ in columns],
            "categories": categories}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, help="Local Insee 3.301 XLSX")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.xlsx:
        blob = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=35) as response:
            blob = response.read()
    checksum = hashlib.sha256(blob).hexdigest()
    if checksum != SOURCE_SHA256:
        raise SystemExit("COFOG Insee XLSX SHA-256 changed: " + checksum)
    result = extract_subfunctions(blob)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8")
    print("COFOG 3.301 subdivisions: 69 codes, 1995–2024, source SHA-256=" + checksum)


if __name__ == "__main__":
    main()
