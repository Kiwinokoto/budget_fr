#!/usr/bin/env python3
"""Reproduce annual SIFA apprentice headcounts (1982–2024) from Insee XLSX T04, sheet T1.

Official XLSX: https://www.insee.fr/fr/statistiques/fichier/8666372/T04%20-%201.4.xlsx
It is *not* a Dares series of apprenticeship contracts started during each year.
No third-party dependencies. No fabricated or interpolated observations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

SOURCE_SHA256 = "93432bd9c0f7e950502544df2de2604b9ec2730e873693b8387b53b2b6800a0d"
SOURCE_ID = "insee_bilan_formation_emploi_2025_t04_sifa_t1"
MAIN_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
FIELDS = ("year", "cap_mention", "bep_certification", "bac_pro", "bac_plus_2",
          "bac_plus_3_or_more", "total", "territory", "source_id")
EXPECTED_HEADERS = ("Années", "CAP et mention complémentaire",
                    "BEP et certification professionnelle", "Diplôme de niveau bac pro",
                    "Diplôme de niveau bac+2", "Diplôme de niveau bac+3 ou plus", "Total")


def read_cells(archive: zipfile.ZipFile, filename: str):
    strings = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    shared = ["".join(node.text or "" for node in item.iter(MAIN_NS+"t"))
              for item in strings.findall(MAIN_NS+"si")]
    root = ET.fromstring(archive.read(filename))
    result = {}
    for row in root.findall(".//"+MAIN_NS+"sheetData/"+MAIN_NS+"row"):
        values = {}
        for cell in row.findall(MAIN_NS+"c"):
            match = re.fullmatch(r"([A-Z]+)\d+", cell.get("r", ""))
            if not match:
                continue
            col = match.group(1)
            if col not in "ABCDEFG" or len(col) != 1:
                continue
            value = cell.find(MAIN_NS+"v")
            if value is None or value.text is None:
                continue
            if cell.get("t") == "s":
                values[col] = shared[int(value.text)]
            elif cell.get("t") in (None, "n"):
                raw = float(value.text)
                if not raw.is_integer():
                    raise ValueError(f"Non-integer in {cell.get('r')}: {value.text}")
                values[col] = int(raw)
            else:
                values[col] = value.text
        result[int(row.get("r"))] = values
    return result


def extract(source: Path, expected_sha256: str = SOURCE_SHA256):
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"Unexpected XLSX checksum: got {digest}, expected {expected_sha256}")
    with zipfile.ZipFile(source) as archive:
        assert "xl/worksheets/sheet2.xml" in archive.namelist()
        cells = read_cells(archive, "xl/worksheets/sheet2.xml")
    if tuple(cells[8].get(c) for c in "ABCDEFG") != EXPECTED_HEADERS:
        raise ValueError(f"Unexpected T1 headers: {cells[8]}")
    if cells[7].get("A") != "effectifs au 31 décembre":
        raise ValueError("Unexpected SIFA counting date")
    if "France hors Mayotte jusqu'en 2010" not in str(cells[53].get("A", "")):
        raise ValueError("Missing expected territorial limitation")
    if cells[54].get("A") != "Source : Depp, enquête SIFA.":
        raise ValueError("Missing expected SIFA provenance")
    results = []
    for year in range(1982, 2025):
        line = cells[year-1982+9]
        if line.get("A") != year:
            raise ValueError(f"Expected {year} in row {year-1982+9}: {line}")
        amounts = [line.get(c) for c in "BCDEFG"]
        if not all(isinstance(a, int) and a >= 0 for a in amounts):
            raise ValueError(f"Invalid numeric row {year}: {amounts}")
        if sum(amounts[:5]) != amounts[5]:
            raise ValueError(f"T1 diploma sums do not reconcile in {year}: {amounts}")
        results.append({
            "year": year,
            "cap_mention": amounts[0],
            "bep_certification": amounts[1],
            "bac_pro": amounts[2],
            "bac_plus_2": amounts[3],
            "bac_plus_3_or_more": amounts[4],
            "total": amounts[5],
            "territory": "france_excluding_mayotte" if year <= 2010 else "france_including_mayotte",
            "source_id": SOURCE_ID,
        })
    if results[13]["year"] != 1995 or results[13]["total"] != 293512:
        raise ValueError("1995 reference is not present")
    if results[-1]["total"] != 1049965 or results[-1]["bac_plus_3_or_more"] != 421000:
        raise ValueError("2024 reference values do not match")
    return results


def write_csv(source: Path, destination: Path):
    rows = extract(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Imported {len(rows)} SIFA observations, {rows[0]['year']}–{rows[-1]['year']}: {destination}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Official XLSX, not committed to Git")
    parser.add_argument("output", type=Path, help="Destination CSV")
    args = parser.parse_args()
    write_csv(args.source, args.output)


if __name__ == "__main__":
    main()
