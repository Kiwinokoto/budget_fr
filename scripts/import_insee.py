#!/usr/bin/env python3
"""Reproduce public-finance series from pinned Insee XLSX; Python standard library only."""
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

SOURCE_URL = "https://www.insee.fr/fr/statistiques/fichier/2381414/econ-fin-pub-rec-dep.xlsx"
SOURCE_SHA256 = "46f401c599cf076956a7b4732d877d57d7f1daea719f7f72397be1dd2f370126"
OUTPUT = Path(__file__).resolve().parents[1] / "data/apu_1960_2025_pct_pib.csv"
FIELDS = (
    "year", "revenue_pct_gdp", "expenditure_pct_gdp", "balance_pct_gdp",
    "gross_debt_pct_gdp", "net_debt_pct_gdp",
    "revenue_ex_imputed_pct_gdp", "expenditure_ex_imputed_pct_gdp"
)
LABELS = {
    "revenue_pct_gdp": "Recettes",
    "expenditure_pct_gdp": "Dépenses",
    "balance_pct_gdp": "Déficit au sens de Maastricht",
    "gross_debt_pct_gdp": "Dette des administrations publiques (brute)2",
    "net_debt_pct_gdp": "Dette nette des administrations publiques3",
    "revenue_ex_imputed_pct_gdp": "dont recettes hors éléments imputés1",
    "expenditure_ex_imputed_pct_gdp": "dont dépenses hors éléments imputés1"
}
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def column_index(reference):
    match = re.match(r"^[A-Z]+", reference)
    if not match:
        raise ValueError("Invalid cell reference")
    col = 0
    for char in match.group():
        col = col * 26 + ord(char) - ord("A") + 1
    return col - 1


def workbook_grid(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall(NS + "si"):
                shared.append("".join(t.text or "" for t in item.iter(NS + "t")))
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        grid = {}
        for row in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
            cells = {}
            for cell in row.findall(NS + "c"):
                v = cell.find(NS + "v")
                inline = cell.find(NS + "is")
                if v is not None:
                    raw = v.text or ""
                elif inline is not None:
                    raw = "".join(t.text or "" for t in inline.iter(NS + "t"))
                else:
                    raw = ""
                if cell.get("t") == "s" and raw:
                    raw = shared[int(raw)]
                cells[column_index(cell.attrib["r"])] = raw
            grid[int(row.attrib["r"])] = cells
        return grid


def extract_rows(blob, expected_years=range(1960, 2026)):
    grid = workbook_grid(blob)
    if grid.get(4, {}).get(0) != "Dépense et recette":
        raise ValueError("Unexpected workbook header")
    year_columns = []
    for col, label in sorted(grid[4].items()):
        if col == 0 or not str(label).strip():
            continue
        match = re.match(r"^(\d{4})(?:\s|$)", str(label))
        if not match:
            raise ValueError("Invalid year column")
        year_columns.append((int(match.group(1)), col))
    if [y for y, _ in year_columns] != list(expected_years):
        raise ValueError("Year coverage changed: inspect workbook")
    by_label = {r[0].strip(): r for r in grid.values() if r.get(0)}
    if not set(LABELS.values()).issubset(by_label):
        raise ValueError("Series labels changed: inspect workbook")
    records = []
    for year, col in year_columns:
        row = {"year": str(year)}
        for key, label in LABELS.items():
            value = by_label[label].get(col, "")
            if value in ("", "nd"):
                if key not in ("gross_debt_pct_gdp", "net_debt_pct_gdp"):
                    raise ValueError(f"Missing {key} in {year}")
                row[key] = ""
                continue
            try:
                row[key] = format(Decimal(str(value)), ".3f")
            except InvalidOperation as exc:
                raise ValueError(f"Invalid {key} in {year}") from exc
        delta = abs(Decimal(row["revenue_pct_gdp"]) -
                    Decimal(row["expenditure_pct_gdp"]) -
                    Decimal(row["balance_pct_gdp"]))
        if delta > Decimal("0.06"):
            raise ValueError(f"Balance consistency fails for {year}: {delta}")
        records.append(row)
    return records


def format_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, help="Use local XLSX instead of downloading")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true",
                        help="Accept a new XLSX only after reviewing revisions")
    args = parser.parse_args()
    if args.xlsx:
        blob = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=35) as response:
            blob = response.read()
    checksum = hashlib.sha256(blob).hexdigest()
    if checksum != SOURCE_SHA256 and not args.allow_source_change:
        raise SystemExit(
            f"Insee XLSX changed (SHA-256 {checksum}); review revisions "
            "before import, then use --allow-source-change explicitly"
        )
    rows = extract_rows(blob)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        stream.write(format_csv(rows))
    print(f"Source: {SOURCE_URL}\nSHA-256: {checksum}\n"
          f"Exported {len(rows)} years: {args.output}")


if __name__ == "__main__":
    main()
