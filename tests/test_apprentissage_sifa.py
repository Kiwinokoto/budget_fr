import csv
import hashlib
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from scripts.import_apprentissage_sifa import (
    EXPECTED_HEADERS, SOURCE_SHA256, extract, FIELDS, SOURCE_ID,
)

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data/apprentissage_sifa_effectifs_1982_2024.csv"
M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


class TestSifaSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            cls.rows = list(reader)
            cls.header = tuple(reader.fieldnames)

    def test_calendar_and_nomenclature(self):
        self.assertEqual(self.header, FIELDS)
        self.assertEqual([int(row["year"]) for row in self.rows], list(range(1982, 2025)))
        self.assertEqual(len(self.rows), 43)
        for row in self.rows:
            total = sum(int(row[k]) for k in FIELDS[1:6])
            self.assertEqual(total, int(row["total"]), row["year"])
            self.assertEqual(row["source_id"], SOURCE_ID)
            self.assertEqual(row["territory"],
                             "france_excluding_mayotte" if int(row["year"]) <= 2010
                             else "france_including_mayotte")

    def test_reference_figures(self):
        rows = {int(r["year"]): r for r in self.rows}
        checks = {
            1982: (233719, 233719, 0),
            1995: (293512, 194485, 4777),
            2018: (448127, 158529, 91249),
            2019: (478803, 160702, 107986),
            2024: (1049965, 191029, 421000),
        }
        for year, (total, cap, bac3) in checks.items():
            with self.subTest(year=year):
                self.assertEqual(int(rows[year]["total"]), total)
                self.assertEqual(int(rows[year]["cap_mention"]), cap)
                self.assertEqual(int(rows[year]["bac_plus_3_or_more"]), bac3)

    def make_fixture(self, corrupt=False):
        ns = "{" + M + "}"
        strings = list(EXPECTED_HEADERS) + [
            "effectifs au 31 décembre",
            "Lecture : au 31 décembre 2024, 421 000 apprentis préparent un diplôme de niveau bac+3 ou plus.",
            "Champ : France hors Mayotte jusqu'en 2010, France à partir de 2011.",
            "Source : Depp, enquête SIFA.",
        ]
        string_ids = {v: i for i, v in enumerate(strings)}
        root = ET.Element(ns+"sst", {"count": str(len(strings)), "uniqueCount": str(len(strings))})
        for label in strings:
            si = ET.SubElement(root, ns+"si")
            ET.SubElement(si, ns+"t").text = label
        ws = ET.Element(ns+"worksheet")
        data = ET.SubElement(ws, ns+"sheetData")
        def put(row, column, value):
            if row not in nodes:
                nodes[row] = ET.SubElement(data, ns+"row", {"r": str(row)})
            r = nodes[row]
            label = f"{column}{row}"
            if isinstance(value, str):
                c = ET.SubElement(r, ns+"c", {"r": label, "t": "s"})
                ET.SubElement(c, ns+"v").text = str(string_ids[value])
            else:
                c = ET.SubElement(r, ns+"c", {"r": label})
                ET.SubElement(c, ns+"v").text = str(value)
        nodes = {}
        put(7, "A", strings[7])
        for c,v in zip("ABCDEFG", EXPECTED_HEADERS):
            put(8,c,v)
        for row in self.rows:
            year = int(row["year"])
            index=year-1982+9
            put(index, "A", year)
            for c,k in zip("BCDEFG",FIELDS[1:7]):
                value=int(row[k])
                if corrupt and year == 2000 and k == "total":
                    value += 1
                put(index, c, value)
        put(52, "A", strings[8])
        put(53, "A", strings[9])
        put(54, "A", strings[10])
        with tempfile.TemporaryDirectory() as dirname:
            out=Path(dirname)/"fixture.xlsx"
            with zipfile.ZipFile(out, "w") as z:
                z.writestr("xl/sharedStrings.xml", ET.tostring(root))
                z.writestr("xl/worksheets/sheet2.xml", ET.tostring(ws))
            raw=out.read_bytes()
            digest=hashlib.sha256(raw).hexdigest()
            with self.assertRaisesRegex(ValueError, "checksum"):
                extract(out)  # original Insee hash is mandatory by default
            if corrupt:
                with self.assertRaisesRegex(ValueError, "do not reconcile"):
                    extract(out, expected_sha256=digest)
            else:
                actual=extract(out, expected_sha256=digest)
                self.assertEqual(actual[-1]["total"], 1049965)
                self.assertEqual(len(actual), 43)

    def test_reproducible_fixture_and_sha_pinning(self):
        self.assertEqual(len(SOURCE_SHA256), 64)
        self.make_fixture()

    def test_incorrect_total_is_rejected(self):
        self.make_fixture(corrupt=True)


if __name__ == "__main__":
    unittest.main()
