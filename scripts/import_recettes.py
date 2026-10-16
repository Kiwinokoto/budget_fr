#!/usr/bin/env python3
"""Reproduce Insee 3.217 national tax and social-levy series, 1995–2025.

No external Python dependencies. Values are rounded to 0.001 billion euros;
the national levies-to-GDP ratio is rounded to 0.001 percentage points.
"""
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

URL = "https://www.insee.fr/fr/statistiques/fichier/8988845/t_3217_fr.xlsx"
SHA256 = "589b94cf953d0fdb6e07b123dcadfd11b831e866096ec0cfb0911d62ae432790"
OUTPUT = Path(__file__).resolve().parents[1] / "data/recettes_1995_2025_bn_eur.csv"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
# Exact source row/label pairs: fail closed when the upstream layout changes.
SERIES = (
    ("levies_bn_eur", 110, "Prélèvements obligatoires = (I)+(II)+(III)+(IV)"),
    ("levies_pct_gdp", 111, "en % du PIB"),
    ("vat_bn_eur", 5, "Taxe sur la valeur ajoutée (TVA) (D211)"),
    ("import_bn_eur", 7, "Impôts et droits sur les importations (D212)"),
    ("product_bn_eur", 10, "Impôts sur les produits (D214)"),
    ("payroll_bn_eur", 39, "Impôts sur les salaires et la main d'œuvre (D291)"),
    ("production_bn_eur", 50, "Impôts divers sur la production (D292)"),
    ("income_bn_eur", 70, "Impôts courants sur le revenu (D51)"),
    ("other_current_bn_eur", 86, "Autres impôts courants (D59)"),
    ("capital_bn_eur", 92, "Impôts en capital (D91r)"),
    ("social_effective_bn_eur", 99, "Cotisations sociales effectives"),
    ("uncollectable_bn_eur", 102, "Impôts et cotisations susceptibles de ne pas être collectés"),
    ("tax_credits_bn_eur", 107, "Crédits d'impôt (IV)"),
    ("irpp_before_credits_bn_eur", 75, "Impôt sur le revenu des personnes physiques (IRPP), avant crédits d'impôt"),
    ("is_before_credits_bn_eur", 78, "Impôt sur les sociétés (IS), avant crédits d'impôt"),
    ("csg_bn_eur", 71, "Contribution sociale généralisée (CSG) (**)"),
    ("crds_bn_eur", 72, "Contribution au remboursement de la dette sociale (CRDS) (**)"),
    ("social_imputed_bn_eur", 100, "Cotisations sociales imputées"),
    ("gross_taxes_social_bn_eur", 104, "Ensemble des impôts et cotisations sociales (I)"),
)
FIELDS = ("year",) + tuple(x[0] for x in SERIES)
POSITIVE = (
    "vat_bn_eur", "import_bn_eur", "product_bn_eur",
    "payroll_bn_eur", "production_bn_eur", "income_bn_eur",
    "other_current_bn_eur", "capital_bn_eur", "social_effective_bn_eur"
)


def _col_index(reference):
    match = re.match(r"^[A-Z]+", reference)
    if match is None:
        raise ValueError("Invalid Excel cell reference")
    result = 0
    for letter in match.group():
        result = result * 26 + ord(letter) - ord("A") + 1
    return result - 1


def grid_from_xlsx(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as workbook:
        strings = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            doc = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
            strings = [
                "".join(n.text or "" for n in item.iter(NS + "t"))
                for item in doc.findall(NS + "si")
            ]
        sheet = ET.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
        grid = {}
        for row in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
            cells = {}
            for cell in row.findall(NS + "c"):
                v = cell.find(NS + "v")
                inline = cell.find(NS + "is")
                if v is not None:
                    raw = v.text or ""
                elif inline is not None:
                    raw = "".join(x.text or "" for x in inline.iter(NS + "t"))
                else:
                    raw = ""
                if cell.get("t") == "s" and raw:
                    raw = strings[int(raw)]
                cells[_col_index(cell.attrib["r"])] = raw
            grid[int(row.attrib["r"])] = cells
    return grid


def extract_rows(blob, expected_years=range(1995, 2026)):
    grid = grid_from_xlsx(blob)
    if list(grid.get(3, {}).values())[:2] == []:
        raise ValueError("Missing header row")
    years = [(int(label), col) for col, label in sorted(grid[3].items())
             if col >= 2 and str(label).strip()]
    if [y for y, _ in years] != list(expected_years):
        raise ValueError("Unexpected Insee tax year coverage")
    for field, row, label in SERIES:
        if grid.get(row, {}).get(1, "").strip() != label:
            raise ValueError("Upstream label changed in row %s for %s" % (row, field))
    records = []
    for year, col in years:
        record = {"year": str(year)}
        for field, row, _ in SERIES:
            raw = grid[row].get(col, "")
            if raw in ("", "N.D.", "nd"):
                raise ValueError("Missing value %s for year %s" % (field, year))
            try:
                value = Decimal(raw)
            except (InvalidOperation, TypeError) as exc:
                raise ValueError("Invalid numeric value %s for %s" % (raw, field)) from exc
            if not value.is_finite():
                raise ValueError("Non-finite %s for %s" % (field, year))
            record[field] = value
        positive = sum(record[k] for k in POSITIVE)
        if abs(positive + record["uncollectable_bn_eur"] +
               record["tax_credits_bn_eur"] - record["levies_bn_eur"]) > Decimal("0.001"):
            raise ValueError("Levies reconciliation failed for %s" % year)
        if abs(positive + record["social_imputed_bn_eur"] -
               record["gross_taxes_social_bn_eur"]) > Decimal("0.001"):
            raise ValueError("Gross levies reconciliation failed for %s" % year)
        if any(record[k] < 0 for k in POSITIVE):
            raise ValueError("Negative component for %s" % year)
        if (record["csg_bn_eur"] + record["crds_bn_eur"] +
            record["irpp_before_credits_bn_eur"] +
            record["is_before_credits_bn_eur"] > record["income_bn_eur"] + Decimal("0.01")):
            raise ValueError("Income tax subcomponents exceed category total in %s" % year)
        records.append({key: str(year) if key == "year"
                        else format(record[key], ".3f") for key in FIELDS})
    return records


def format_csv(records):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path)
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
        raise SystemExit("Source SHA-256 changed (%s); audit upstream revision before importing" % digest)
    rows = extract_rows(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        stream.write(format_csv(rows))
    print("Insee 3.217 SHA256=%s years=%s–%s output=%s" %
          (digest, rows[0]["year"], rows[-1]["year"], args.output))


if __name__ == "__main__":
    main()
