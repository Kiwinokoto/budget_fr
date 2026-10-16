import csv
from decimal import Decimal
from pathlib import Path
import unittest

from scripts.import_interest import HEADER, SHA256, column, format_csv

FILE = Path(__file__).resolve().parents[1] / "data/interets_apu_1959_2025_bn_eur.csv"


class TestGeneralGovernmentInterest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with FILE.open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source)
            cls.columns = reader.fieldnames
            cls.rows = list(reader)

    def test_coverage_and_types(self):
        self.assertEqual(self.columns, HEADER.strip().split(","))
        self.assertEqual([int(x["year"]) for x in self.rows], list(range(1959, 2026)))
        for item in self.rows:
            amounts = [Decimal(item[key]) for key in self.columns[1:]]
            self.assertTrue(all(value.is_finite() and value > 0 for value in amounts))
            self.assertLess(amounts[0], amounts[2])
            self.assertLess(amounts[1], amounts[2])

    def test_published_2025_values_and_pre_euro_years(self):
        self.assertEqual(self.rows[-1]["interest_d41_bn_eur"], "65.7209")
        self.assertEqual(self.rows[-1]["interest_ex_fisim_bn_eur"], "64.6519")
        self.assertEqual(self.rows[-1]["total_expenditure_bn_eur"], "1714.1117")
        self.assertEqual(self.rows[0]["interest_d41_bn_eur"], "0.5145")
        self.assertEqual(self.rows[21]["year"], "1980")
        self.assertEqual(self.rows[21]["interest_d41_bn_eur"], "5.5151")

    def test_interest_concepts_do_not_have_fixed_order(self):
        self.assertGreater(Decimal(self.rows[0]["interest_ex_fisim_bn_eur"]),
                           Decimal(self.rows[0]["interest_d41_bn_eur"]))
        self.assertLess(Decimal(self.rows[-1]["interest_ex_fisim_bn_eur"]),
                        Decimal(self.rows[-1]["interest_d41_bn_eur"]))

    def test_importer_structure(self):
        self.assertEqual(len(SHA256), 64)
        self.assertEqual(column(2), "C")
        self.assertEqual(column(68), "BQ")
        self.assertEqual(format_csv([(2025, Decimal("65.7209"), Decimal("64.6519"),
            Decimal("1714.1117"))]), HEADER + "2025,65.7209,64.6519,1714.1117\n")


if __name__ == "__main__":
    unittest.main()
