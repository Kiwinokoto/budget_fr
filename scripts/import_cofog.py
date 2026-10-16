#!/usr/bin/env python3
"""Import Insee COFOG table 3.301 (consolidated S13 functions) using Python stdlib."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import io
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

SOURCE_URL = "https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx"
SOURCE_SHA256 = "ce36c71eafebdcbd941ef5cb74f10e79734fa4e1cc0dc1e97d84e321412c5ce5"
OUTPUT = Path(__file__).resolve().parents[1] / "data/cofog_1995_2024_bn_eur.csv"
FIELDS = ("year", "total_bn_eur") + tuple("gf%02d" % i for i in range(1, 11))
CODES = ("_Z",) + tuple("GF%02d" % i for i in range(1, 11))
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
TOTAL_LABEL = "Total des dépenses des administrations publiques (*)"


def _column(reference):
    prefix = re.match(r"^[A-Z]+", reference)
    if not prefix:
        raise ValueError("Bad cell reference")
    index = 0
    for letter in prefix.group():
        index = index * 26 + ord(letter) - ord("A") + 1
    return index - 1


def _grid(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [
                "".join(text.text or "" for text in item.iter(NS + "t"))
                for item in strings.findall(NS + "si")
            ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows = {}
        for line in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
            cells = {}
            for cell in line.findall(NS + "c"):
                value = cell.find(NS + "v")
                inline = cell.find(NS + "is")
                if value is not None:
                    raw = value.text or ""
                elif inline is not None:
                    raw = "".join(t.text or "" for t in inline.iter(NS + "t"))
                else:
                    raw = ""
                if cell.get("t") == "s" and raw:
                    raw = shared[int(raw)]
                cells[_column(cell.attrib["r"])] = raw
            rows[int(line.attrib["r"])] = cells
        return rows


def extract_rows(blob, expected_years=range(1995, 2025)):
    grid = _grid(blob)
    years = [
        (int(value), col)
        for col, value in sorted(grid.get(4, {}).items())
        if col > 3 and str(value or "").strip()
    ]
    if [year for year, _ in years] != list(expected_years):
        raise ValueError("Unexpected COFOG year coverage")
    series = {}
    for row in grid.values():
        if row.get(0) == "OTE" and row.get(1) == TOTAL_LABEL:
            code = row.get(2)
            if code in CODES:
                if code in series:
                    raise ValueError("Duplicate top-level COFOG series: " + code)
                series[code] = row
    if set(series) != set(CODES):
        raise ValueError("Missing top-level COFOG series")
    records = []
    for year, col in years:
        item = {"year": str(year)}
        values = []
        for code in CODES:
            try:
                number = Decimal(str(series[code][col]))
            except (KeyError, InvalidOperation) as exc:
                raise ValueError("Missing/invalid COFOG value %s in %s" % (code, year)) from exc
            if not number.is_finite() or number < 0:
                raise ValueError("Invalid negative/nonfinite COFOG amount")
            values.append(number)
        if abs(values[0] - sum(values[1:])) > Decimal("0.015"):
            raise ValueError("COFOG categories do not reconcile with total in %s" % year)
        for field, number in zip(FIELDS[1:], values):
            item[field] = format(number, ".3f")
        records.append(item)
    return records


def format_csv(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, help="Read a local, previously verified XLSX")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true",
                        help="Allow explicit analysis of a new source; review output before committing")
    args = parser.parse_args()
    if args.xlsx:
        blob = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=35) as response:
            blob = response.read()
    checksum = hashlib.sha256(blob).hexdigest()
    if checksum != SOURCE_SHA256 and not args.allow_source_change:
        raise SystemExit("COFOG source SHA-256 changed (%s); audit source first" % checksum)
    records = extract_rows(blob)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        stream.write(format_csv(records))
    print("COFOG 3.301; SHA-256=%s; years=%s–%s; output=%s" %
          (checksum, records[0]["year"], records[-1]["year"], args.output))


if __name__ == "__main__":
    main()
