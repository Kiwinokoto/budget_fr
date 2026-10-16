#!/usr/bin/env python3
"""Import Insee 3.102: nominal, consolidated Maastricht debt by instrument and S13 sector.

1995–2025, end-of-year stocks, billion current EUR. The XLSX is not committed.
Source: https://www.insee.fr/fr/statistiques/8988843 (28 August 2026, base 2020).
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

URL = "https://www.insee.fr/fr/statistiques/fichier/8988843/t_3102_fr.xlsx"
SHA256 = "6c8beca5fb0ac72754887d8a871a83eda6f8523ca6c903c1bc898f8cfe749b49"
OUTPUT = Path(__file__).resolve().parents[1] / "data/dette_maastricht_instruments_1995_2025_bn_eur.csv"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
YEARS = tuple(range(1995, 2026))
SECTOR_ROWS = {"S13": 6, "S1311": 15, "S13111": 24, "S13112": 33, "S1313": 42, "S1314": 51}
CODES = ("F2N", "F31_32", "F31", "F32", "F41", "F42", "GD")
FIELDS = ("year", "sector", "deposits_bn_eur", "securities_bn_eur", "short_securities_bn_eur",
          "long_securities_bn_eur", "short_loans_bn_eur", "long_loans_bn_eur", "maastricht_bn_eur")
TOL = Decimal("0.25")  # components rounded independently to 0.1 billion
# In the official 2026 XLSX, S1314/F2N has no value in any of the 31 years.
# Preserve as missing in CSV; do not publish an inferred zero.
UNREPORTED = {("S1314", "F2N")}


def col_name(number):
    result = ""
    while number:
        number, rem = divmod(number - 1, 26)
        result = chr(65 + rem) + result
    return result


def grid(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            strings = [
                "".join(t.text or "" for t in item.iter(NS + "t"))
                for item in root.findall(NS + "si")
            ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows = {}
        for element in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
            cells = {}
            for cell in element.findall(NS + "c"):
                match = re.match(r"^[A-Z]+", cell.attrib["r"])
                if match is None:
                    raise ValueError("Malformed Excel cell reference")
                val, inline = cell.find(NS + "v"), cell.find(NS + "is")
                raw = (val.text or "") if val is not None else (
                    "".join(t.text or "" for t in inline.iter(NS + "t"))
                    if inline is not None else "")
                if cell.get("t") == "s" and raw:
                    raw = strings[int(raw)]
                cells[match.group()] = raw
            rows[int(element.attrib["r"])] = cells
        return rows


def extract(blob):
    rows = grid(blob)
    if not rows.get(1, {}).get("A", "").startswith("3.102 Dette des administrations publiques"):
        raise ValueError("Unexpected Insee title")
    if rows.get(2, {}).get("A") != "Unité : Milliard d'euros":
        raise ValueError("Unexpected Insee unit")
    expected_cols = [col_name(i) for i in range(3, 34)]
    if [key for key, value in rows.get(4, {}).items() if value and key not in ("A", "B")] != expected_cols:
        raise ValueError("Unexpected year columns")
    for year, col in zip(YEARS, expected_cols):
        if rows[4].get(col) != str(year):
            raise ValueError("Unexpected year: %s" % year)

    records = []
    for sector, first in SECTOR_ROWS.items():
        heading = rows.get(first - 1, {}).get("B", "") if sector == "S13" else rows.get(first - 1, {}).get("B", "")
        if not heading.startswith(sector + " - "):
            raise ValueError("Unexpected sector heading %s" % sector)
        for offset, code in enumerate(CODES):
            if rows.get(first + offset, {}).get("A") != code:
                raise ValueError("Missing/reordered row %s %s" % (sector, code))
        for year, col in zip(YEARS, expected_cols):
            values = []
            for offset, code in enumerate(CODES):
                raw = rows[first + offset].get(col)
                if (sector, code) in UNREPORTED:
                    if raw not in (None, ""):
                        raise ValueError("Previously unreported S1314/F2N now has data: %s" % year)
                    values.append(None)
                    continue
                if raw in (None, ""):
                    raise ValueError("Missing %s %s %s" % (year, sector, code))
                try:
                    number = Decimal(raw)
                except (InvalidOperation, TypeError) as exc:
                    raise ValueError("Invalid %s %s %s" % (year, sector, code)) from exc
                if not number.is_finite() or number < 0:
                    raise ValueError("Negative/nonfinite amount %s %s %s" % (year, sector, code))
                values.append(number)
            deposit, securities, short_sec, long_sec, short_loan, long_loan, total = values
            if abs(securities - short_sec - long_sec) > TOL:
                raise ValueError("Securities breakdown fails: %s %s" % (year, sector))
            # For S1314, independently published GD and other instruments
            # reconcile; the source omits deposits, which CSV keeps blank.
            known = deposit if deposit is not None else Decimal(0)
            if abs(total - known - securities - short_loan - long_loan) > TOL:
                raise ValueError("Instrument breakdown fails: %s %s" % (year, sector))
            records.append((year, sector, *values))

    lookup = {(r[0], r[1]): r for r in records}
    for year in YEARS:
        total = lookup[(year, "S13")]
        central = lookup[(year, "S1311")]
        state, odac, local, social = (
            lookup[(year, s)] for s in ("S13111", "S13112", "S1313", "S1314")
        )
        for index in range(2, 9):
            if abs(total[index] - sum(
                (p[index] for p in (state, odac, local, social) if p[index] is not None),
                Decimal(0),
            )) > TOL * 2:
                raise ValueError("Sector breakdown fails: %s %s" % (year, FIELDS[index]))
            if abs(central[index] - state[index] - odac[index]) > TOL:
                raise ValueError("Central subsector breakdown fails: %s %s" % (year, FIELDS[index]))
    if lookup[(2025, "S13")][-1].quantize(Decimal(".1")) != Decimal("3460.1"):
        raise ValueError("2025 audited anchor changed")
    return records


def format_csv(records):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(FIELDS)
    for year, sector, *amounts in records:
        writer.writerow((year, sector, *(
            format(value, ".1f") if value is not None else "" for value in amounts
        )))
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, help="Already-downloaded official workbook")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true",
                        help="Experimental audit only; review differences before committing")
    args = parser.parse_args()
    blob = args.xlsx.read_bytes() if args.xlsx else urllib.request.urlopen(URL, timeout=35).read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256 and not args.allow_source_change:
        raise SystemExit("Insee 3.102 SHA-256 changed (%s); audit first" % digest)
    records = extract(blob)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(format_csv(records), encoding="utf-8", newline="")
    print("Insee 3.102 SHA256=%s; 1995–2025; %d records; output=%s" %
          (digest, len(records), args.output))


if __name__ == "__main__":
    main()
