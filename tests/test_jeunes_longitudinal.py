import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT / "data" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
class TestJeunesLongitudinal(unittest.TestCase):
    def test_scolarisation(self):
        rows = load("jeunes_scolarisation_1986_2023_insee.csv")
        self.assertEqual(len(rows),38)
        self.assertEqual([int(row["year"]) for row in rows],list(range(1986,2024)))
        self.assertEqual((rows[0]["age_18_pct"],rows[0]["age_21_pct"]),("61.7","20.7"))
        self.assertEqual((rows[9]["age_18_pct"],rows[9]["age_21_pct"]),("84.8","44.8"))
        self.assertEqual((rows[32]["age_18_pct"],rows[32]["age_21_pct"]),("78.7","45.0"))
        self.assertEqual([rows[-1][key] for key in ("age_18_pct","age_21_pct","age_25_pct","age_29_pct")],["78.6","50.9","13.4","4.1"])
        for row in rows:
            self.assertEqual(row["source_id"],"insee_fps2025_f7_fig1")
            for key in ("age_18_pct","age_21_pct","age_25_pct","age_29_pct"):
                self.assertRegex(row[key],r"^\d+\.\d$")
                self.assertLessEqual(float(row[key]),100)
    def test_workstudy(self):
        rows=load("jeunes_cumul_emploi_etudes_2003_2023_insee.csv")
        self.assertEqual(len(rows),21)
        self.assertEqual([int(row["year"]) for row in rows],list(range(2003,2024)))
        self.assertEqual([rows[0][key] for key in ("age_15_29_pct","age_15_19_pct","age_20_24_pct")],["11.7","7.0","18.9"])
        self.assertEqual(rows[15]["age_15_29_pct"],"15.2")
        self.assertEqual(rows[18]["age_15_29_pct"],"20.0")
        self.assertEqual([rows[-1][key] for key in ("age_15_29_pct","age_15_19_pct","age_20_24_pct")],["22.3","12.3","40.8"])
        for row in rows:
            self.assertEqual(row["source_id"],"insee_bfe2025_f5_fig1")
    def test_provenance_and_breaks(self):
        sources=(ROOT/"JEUNES_CONTEXTE_SOURCES.md").read_text()
        doc=(ROOT/"apprentissage-contexte.html").read_text()
        for sha in ("881ea0b49f9c1937ef536728678082336392be6729bdec160d83ed1376664340","62b962d7f75dff49b60508595c8e0b4f9a63b9d41b187833c727391d46767288"):
            self.assertIn(sha,sources)
        for year in ("1999","2018","2014","2021"):
            self.assertIn(year,sources)
        self.assertIn("dénominateurs",doc)
        self.assertIn("reprise d'études",doc)
        self.assertIn('src="/jeunes-histoire.js"',doc)
