import csv
import pathlib
import unittest

PATH = pathlib.Path(__file__).resolve().parents[1] / "data/apu_1995_2025_pct_pib.csv"

class TestData(unittest.TestCase):
    def test_apu_ratios(self):
        with PATH.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual([int(r["year"]) for r in rows], list(range(1995, 2026)))
        for row in rows:
            revenue = float(row["revenue_pct_gdp"])
            spending = float(row["expenditure_pct_gdp"])
            balance = float(row["balance_pct_gdp"])
            self.assertGreater(revenue, 0)
            self.assertGreater(spending, 0)
            self.assertLessEqual(abs((revenue - spending) - balance), 0.11000001, row["year"])
        self.assertEqual(float(rows[-1]["revenue_pct_gdp"]), 52.2)
        self.assertEqual(float(rows[-1]["expenditure_pct_gdp"]), 57.3)

if __name__ == "__main__":
    unittest.main()
