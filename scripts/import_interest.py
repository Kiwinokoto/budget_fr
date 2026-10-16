#!/usr/bin/env python3
"""Reproduce Insee 3.201 annual general government interest expenditure, 1959–2025.

Official source: S13 public expenditure, not solely the State or Maastricht
debt outstanding. Two interest concepts differ because of FISIM corrections.
No third-party dependencies; original workbook is not committed.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import io
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

URL = "https://www.insee.fr/fr/statistiques/fichier/8988845/t_3201_fr.xlsx"
SHA256 = "487d4299a5bac8d616000952fd012a0eb6d251a3586508165fc37d64a73a397a"
OUTPUT = Path(__file__).resolve().parents[1] / "data/interets_apu_1959_2025_bn_eur.csv"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
HEADER = "year,interest_d41_bn_eur,interest_ex_fisim_bn_eur,total_expenditure_bn_eur\n"
FIELDS = (
    (12, "Intérêts (D41)"),
    (13, "Intérêts hors correction au titre des services d'intermédiation financière indirectement mesurés (D41G)"),
    (27, "Total des dépenses"),
)


def column(index):
    """0-indexed Excel column -> letter."""
    result = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        result = chr(ord("A") + rem) + result
    return result


def parse_rows(blob, extra_rows=()):
    with zipfile.ZipFile(io.BytesIO(blob)) as book:
        shared = []
        if "xl/sharedStrings.xml" in book.namelist():
            root = ET.fromstring(book.read("xl/sharedStrings.xml"))
            shared = [
                "".join(t.text or "" for t in s.iter(NS + "t"))
                for s in root.findall(NS + "si")
            ]
        page = ET.fromstring(book.read("xl/worksheets/sheet1.xml"))
        rows = {}
        for row in page.findall(".//" + NS + "sheetData/" + NS + "row"):
            idx = int(row.get("r"))
            if idx not in (3, 12, 13, 27, *extra_rows):
                continue
            cells = {}
            for cell in row.findall(NS + "c"):
                val = cell.find(NS + "v")
                ins = cell.find(NS + "is")
                if val is not None:
                    raw = val.text or ""
                elif ins is not None:
                    raw = "".join(t.text or "" for t in ins.iter(NS + "t"))
                else:
                    raw = ""
                if cell.get("t") == "s" and raw:
                    raw = shared[int(raw)]
                ref = re.match(r"^[A-Z]+", cell.attrib["r"])
                if not ref:
                    raise ValueError("Malformed cell address")
                cells[ref.group()] = raw
            rows[idx] = cells
    if set(rows) != {3, 12, 13, 27, *extra_rows}:
        raise ValueError("Source table rows have changed")
    for row, label in FIELDS:
        if rows[row].get("B", "").strip() != label:
            raise ValueError("Unexpected Insee row label at %d" % row)
    return rows


def extract(blob):
    rows = parse_rows(blob)
    expected_columns = [column(2 + year - 1959) for year in range(1959, 2026)]
    year_headers = [
        (col, str(year)) for year, col in zip(range(1959, 2026), expected_columns)
    ]
    for col, year in year_headers:
        if rows[3].get(col) != year:
            raise ValueError("Unexpected year label for %s: expected %s" % (col, year))
    nonempty_years = {key for key, value in rows[3].items()
                      if value.strip().isdigit() and key not in ("A", "B")}
    if nonempty_years != set(expected_columns):
        raise ValueError("Source added/removed historical years")
    records = []
    for year, col in zip(range(1959, 2026), expected_columns):
        values = []
        for source_row, _ in FIELDS:
            raw = rows[source_row].get(col)
            if not raw:
                raise ValueError("Missing interest/expenditure data for %s" % year)
            try:
                value = Decimal(raw)
            except (InvalidOperation, TypeError) as exc:
                raise ValueError("Non-numeric data in %s" % year) from exc
            if not value.is_finite() or value <= 0:
                raise ValueError("Invalid non-positive data in %s" % year)
            values.append(value)
        d41, ex_fisim, expenditure = values
        if d41 >= expenditure or ex_fisim >= expenditure:
            raise ValueError("Interest cannot exceed expenditure in %d" % year)
        records.append((year, *values))
    return records


def format_csv(records):
    return HEADER + "".join(
        "%d,%s\n" % (year, ",".join(format(value, ".4f") for value in amounts))
        for year, *amounts in records
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, help="Use a downloaded official XLSX")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true")
    args = parser.parse_args()
    if args.xlsx:
        data = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=35) as response:
            data = response.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != SHA256 and not args.allow_source_change:
        raise SystemExit("XLSX SHA256 changed: %s; audit upstream before importing" % digest)
    records = extract(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(format_csv(records), encoding="utf-8")
    print("Insee 3.201 SHA256=%s; years=1959–2025; output=%s" %
          (digest, args.output))


if __name__ == "__main__":
    main()
