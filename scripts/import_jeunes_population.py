#!/usr/bin/env python3
"""Import ages 15–29 at 1 Jan 2024 (France) from official Insee XLSX, pinned SHA256.

Original source: https://www.insee.fr/fr/statistiques/fichier/8313981/Pop1janv_age.xlsx
Excel sheet 2024 is xl/worksheets/sheet119.xml in this *pinned* archive.
No third-party packages and no original XLSX committed.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

SHA256 = "223e5d4699d1b99b20b1e81a7f75dec961031272d74c4cd429fb9466fc8f574d"
MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
FIELDS = ("year","age","total","men","women","territory","source_id")
SOURCE_ID="insee_bilan_demographique_2024_pop1janv_age"


def extract(source:Path, expected_sha=SHA256):
    raw=source.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest != expected_sha:
        raise ValueError(f"Source XLSX checksum mismatch: {digest} != {expected_sha}")
    with ZipFile(source) as z:
        shared=ET.fromstring(z.read("xl/sharedStrings.xml"))
        words=["".join(t.text or "" for t in si.iter(MAIN+"t"))
               for si in shared.findall(MAIN+"si")]
        root=ET.fromstring(z.read("xl/worksheets/sheet119.xml"))
    indexed={}
    for row in root.findall(".//"+MAIN+"sheetData/"+MAIN+"row"):
        cells={}
        for c in row.findall(MAIN+"c"):
            m=re.fullmatch(r"([A-H])(\d+)",c.get("r",""))
            if not m:continue
            v=c.find(MAIN+"v")
            if v is None:continue
            value=words[int(v.text)] if c.get("t")=="s" else v.text
            cells[m.group(1)]=value
        indexed[int(row.get("r"))]=cells
    if "2024" not in indexed[1]["A"]:
        raise ValueError("Unexpected workbook year")
    if indexed[4].get("F") != "France":
        raise ValueError("Missing population territory 'France'")
    if indexed[5].get("B") != "Âge en années révolues" or indexed[5].get("F") != "Ensemble ":
        raise ValueError("Unexpected source age / sex headers")
    rows=[]
    for age in range(15,30):
        sheetrow=age+7
        cell=indexed[sheetrow]
        if cell.get("B","").strip() != str(age):
            raise ValueError(f"Unexpected age in row {sheetrow}")
        vals=[int(cell[c]) for c in ("F","G","H")]
        if min(vals)<0 or vals[0] != vals[1]+vals[2]:
            raise ValueError(f"Population sex sums differ in age {age}")
        rows.append(dict(year=2024,age=age,total=vals[0],men=vals[1],women=vals[2],
                         territory="france",source_id=SOURCE_ID))
    def summ(lo,hi):
        return sum(r["total"] for r in rows if lo<=r["age"]<=hi)
    if summ(18,25)!=6375226 or summ(15,24)!=8209108 or summ(18,29)!=9446471:
        raise ValueError("Reference population aggregates do not match official vintage")
    return rows


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xlsx",type=Path)
    ap.add_argument("csv_path",type=Path)
    a=ap.parse_args()
    rows=extract(a.xlsx)
    a.csv_path.parent.mkdir(parents=True,exist_ok=True)
    with a.csv_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
        w.writeheader();w.writerows(rows)
    print(f"Reproduced {len(rows)} ages, 2024: {a.csv_path}")


if __name__=="__main__":main()
