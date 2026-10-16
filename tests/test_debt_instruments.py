"""Tests for Insee 3.102 annual debt composition and reporting gaps."""
import csv
from decimal import Decimal
from pathlib import Path
import unittest
import zipfile

from scripts import import_debt_instruments as debt

DATA = Path(__file__).resolve().parents[1] / "data/dette_maastricht_instruments_1995_2025_bn_eur.csv"


class TestDebtInstruments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.columns = reader.fieldnames
            cls.rows = list(reader)
        cls.lookup = {(int(r["year"]), r["sector"]): r for r in cls.rows}

    def test_coverage_and_unique_keys(self):
        self.assertEqual(cls_fields := list(debt.FIELDS), self.columns)
        self.assertEqual(len(self.rows), len(debt.YEARS) * len(debt.SECTOR_ROWS))
        self.assertEqual(set(self.lookup), {
            (year, sector) for year in debt.YEARS for sector in debt.SECTOR_ROWS
        })
        self.assertEqual(len(self.lookup), len(self.rows))

    def test_omitted_social_deposits_remain_blank(self):
        for year in debt.YEARS:
            for sector in debt.SECTOR_ROWS:
                r = self.lookup[(year, sector)]
                for name in debt.FIELDS[2:]:
                    raw = r[name]
                    if sector == "S1314" and name == "deposits_bn_eur":
                        self.assertEqual(raw, "")
                    else:
                        self.assertTrue(raw, (year, sector, name))
                        value = Decimal(raw)
                        self.assertTrue(value.is_finite())
                        self.assertGreaterEqual(value, Decimal(0))

    def test_accounting_identities(self):
        tol = debt.TOL
        for year in debt.YEARS:
            number = lambda sector, field: Decimal(self.lookup[(year, sector)][field] or "0")
            for sector in debt.SECTOR_ROWS:
                self.assertLessEqual(abs(
                    number(sector, "securities_bn_eur")
                    - number(sector, "short_securities_bn_eur")
                    - number(sector, "long_securities_bn_eur")
                ), tol)
                self.assertLessEqual(abs(
                    number(sector, "maastricht_bn_eur")
                    - number(sector, "deposits_bn_eur")
                    - number(sector, "securities_bn_eur")
                    - number(sector, "short_loans_bn_eur")
                    - number(sector, "long_loans_bn_eur")
                ), tol)
            for field in debt.FIELDS[2:]:
                self.assertLessEqual(abs(
                    number("S13", field) - sum(
                        (number(s, field) for s in ("S13111", "S13112", "S1313", "S1314")),
                        Decimal(0),
                    )
                ), tol * 2)
                self.assertLessEqual(abs(
                    number("S1311", field) - number("S13111", field) - number("S13112", field)
                ), tol)

    def test_2025_official_anchors(self):
        row = self.lookup[(2025, "S13")]
        expected = {
            "maastricht_bn_eur": "3460.1",
            "securities_bn_eur": "3096.2",
            "deposits_bn_eur": "42.8",
            "short_securities_bn_eur": "270.9",
            "long_securities_bn_eur": "2825.3",
            "short_loans_bn_eur": "13.7",
            "long_loans_bn_eur": "307.5",
        }
        for key, value in expected.items():
            self.assertEqual(row[key], value)
        self.assertEqual(len(debt.SHA256), 64)

    def test_corrupt_input_is_rejected(self):
        with self.assertRaises((ValueError, zipfile.BadZipFile)):
            debt.extract(b"not an xlsx")


if __name__ == "__main__":
    unittest.main()
