#!/usr/bin/env python3
"""Insee CND.101: national-accounts distribution of *product taxes*, not VAT alone.

Source covers 2020–2023, vintiles V1–V20; units billions of current euros.
The CSV is positive amounts paid/attributed, while original source uses negatives.
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

URL = "https://www.insee.fr/fr/statistiques/fichier/8574663/T_CND_101.xlsx"
SHA256 = "8e4d2ec005e9351f7105c796ac2e0ae8afc1f53b70b165d04f9387ed8cf838ef"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/taxes_produits_cnd_2020_2023.csv"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ROW_LABEL = "Taxes sur les produits (TVA, TICPE, acises, DMTO, etc.)"
HEADER = "year,vingtile,product_taxes_bn_eur\n"


def read_row(archive, name, target, shared):
    sheet = ET.fromstring(archive.read(name))
    for row in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
        if int(row.get("r")) != target:
            continue
        values = {}
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
            column = re.match(r"^[A-Z]+", cell.attrib["r"])
            if not column:
                raise ValueError("Bad cell reference")
            values[column.group()] = raw
        return values
    raise ValueError("Missing sheet row " + str(target))


def extract(blob):
    records = []
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [
                "".join(t.text or "" for t in item.iter(NS + "t"))
                for item in root.findall(NS + "si")
            ]
        for year, sheet_number in zip(range(2020, 2024), range(2, 6)):
            sheet = "xl/worksheets/sheet%d.xml" % sheet_number
            headings = read_row(archive, sheet, 1, shared)
            values = read_row(archive, sheet, 16, shared)
            if headings.get("A") != "Nature des revenus et transferts":
                raise ValueError("Unexpected CND.101 sheet header")
            if values.get("A") != ROW_LABEL:
                raise ValueError("Unexpected product-taxes label")
            total = Decimal(values["V"])
            if total >= 0:
                raise ValueError("Product taxes should be negative in source")
            parts = []
            for i in range(1, 21):
                col = chr(65 + i)
                if headings.get(col) != "V%d" % i:
                    raise ValueError("Vintile headings changed")
                try:
                    tax = Decimal(values[col])
                except (KeyError, InvalidOperation) as exc:
                    raise ValueError("Invalid tax value") from exc
                if not tax.is_finite() or tax >= 0:
                    raise ValueError("Product taxes are missing/invalid")
                parts.append(tax)
                records.append((year, i, -tax))
            # Official published values rounded to 0.1 billion: 20 rounded
            # components can deviate from the published total (2022: 0.1).
            if abs(sum(parts) - total) > Decimal("0.5"):
                raise ValueError("Product-tax vintiles do not match total: %d" % year)
    return records


def csv_text(records):
    return HEADER + "".join(
        "%d,%d,%.1f\n" % (year, ving, value)
        for year, ving, value in records
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true")
    args = parser.parse_args()
    if args.xlsx:
        blob = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=35) as response:
            blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256 and not args.allow_source_change:
        raise SystemExit("Insee CND.101 XLSX changed SHA-256 (%s); audit first" % digest)
    content = csv_text(extract(blob))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print("CND.101 SHA-256=%s; years=2020–2023; CSV=%s" % (digest, args.output))


if __name__ == "__main__":
    main()
