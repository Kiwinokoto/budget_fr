#!/usr/bin/env python3
"""Extrait deux tableaux Insee publiés, sans interpoler les années ni les âges."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree as ET
from zipfile import ZipFile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SOURCES = {
    "scolarisation": (
        "https://www.insee.fr/fr/statistiques/fichier/8612518/FPORSOC25-F7.xlsx",
        "881ea0b49f9c1937ef536728678082336392be6729bdec160d83ed1376664340",
        1986,
        2023,
        ("18 ans", "21 ans", "25 ans", "29 ans"),
        ("age_18_pct", "age_21_pct", "age_25_pct", "age_29_pct"),
        "insee_fps2025_f7_fig1",
        "jeunes_scolarisation_1986_2023_insee.csv",
    ),
    "cumul": (
        "https://www.insee.fr/fr/statistiques/fichier/8305508/BFE2025-F5.xlsx",
        "62b962d7f75dff49b60508595c8e0b4f9a63b9d41b187833c727391d46767288",
        2003,
        2023,
        ("Ensemble des 15-29 ans", "15-19 ans", "20-24 ans"),
        ("age_15_29_pct", "age_15_19_pct", "age_20_24_pct"),
        "insee_bfe2025_f5_fig1",
        "jeunes_cumul_emploi_etudes_2003_2023_insee.csv",
    ),
}


def sheet_cells(original: bytes) -> dict[str, str]:
    with ZipFile(io.BytesIO(original)) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [
                "".join(t.text or "" for t in node.findall(".//m:t", NS))
                for node in root.findall("m:si", NS)
            ]
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        result: dict[str, str] = {}
        for c in root.findall(".//m:sheetData/m:row/m:c", NS):
            address = c.get("r")
            value = c.find("m:v", NS)
            text = value.text if value is not None and value.text is not None else ""
            if c.get("t") == "s" and text:
                text = shared[int(text)]
            elif c.get("t") == "inlineStr":
                text = "".join(t.text or "" for t in c.findall(".//m:t", NS))
            if address:
                result[address] = text
        return result


def build(kind: str, file_path: Path | None, out_dir: Path) -> Path:
    url, expected_sha, first, last, headers, names, source_id, filename = SOURCES[kind]
    original = file_path.read_bytes() if file_path is not None else urlopen(url, timeout=35).read()
    digest = hashlib.sha256(original).hexdigest()
    if digest != expected_sha:
        raise ValueError(f"{kind}: SHA-256 source modifiée ({digest}), audit nécessaire")
    cells = sheet_cells(original)
    assert cells["A1"].startswith("Figure 1"), f"{kind}: feuille inattendue"
    assert cells["A3"] == "Année"
    for col, label in zip("BCDE", headers, strict=False):
        assert cells[f"{col}3"] == label, (kind, col, cells.get(f"{col}3"))
    output = out_dir / filename
    data = []
    for year in range(first, last + 1):
        row_num = year - first + 4
        raw_year = cells[f"A{row_num}"]
        assert raw_year.rstrip("p") == str(year), (kind, row_num, raw_year)
        nums = []
        for col in "BCDE"[: len(names)]:
            raw = cells[f"{col}{row_num}"]
            val = Decimal(raw)
            assert 0 <= val <= 100 and (val * 10 - (val * 10).to_integral_value()).copy_abs() < Decimal("0.000001"), (year, col, raw)
            nums.append(f"{val.quantize(Decimal('0.1')):.1f}")
        data.append([year, *nums, source_id])
    assert len(data) == last - first + 1
    if kind == "scolarisation":
        assert data[0][1:3] == ["61.7", "20.7"] and data[-1][1:3] == ["78.6", "50.9"]
    else:
        assert data[0][1:3] == ["11.7", "7.0"] and data[-1][1:3] == ["22.3", "12.3"]
    out_dir.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(["year", *names, "source_id"])
        writer.writerows(data)
    print(f"{kind}: {len(data)} années, SHA-256 source {digest}, CSV {output}")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scolarisation-xlsx", type=Path)
    parser.add_argument("--cumul-xlsx", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    opts = parser.parse_args()
    build("scolarisation", opts.scolarisation_xlsx, opts.output_dir)
    build("cumul", opts.cumul_xlsx, opts.output_dir)


if __name__ == "__main__":
    main()
