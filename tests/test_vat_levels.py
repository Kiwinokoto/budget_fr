import csv
from decimal import Decimal
from pathlib import Path
import unittest

from scripts.import_cnd_product_taxes import HEADER, SHA256, csv_text, extract

DATA = Path(__file__).resolve().parents[1] / "data"
VAT = DATA / "tva_effort_bdf_2001.csv"
PRODUCT = DATA / "taxes_produits_cnd_2020_2023.csv"


class TestVatLevelsBdf2001(unittest.TestCase):
    def test_source_table_3_4_6(self):
        with VAT.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames,
                ["decile", "vat_eur_per_household",
                 "vat_pct_gross_disposable_income", "vat_pct_consumption"])
            r = list(reader)
        self.assertEqual([int(x["decile"]) for x in r], list(range(1, 11)))
        self.assertEqual(r[0]["vat_eur_per_household"], "1308")
        self.assertEqual(r[-1]["vat_eur_per_household"], "3588")
        self.assertEqual(r[0]["vat_pct_gross_disposable_income"], "11.52")
        self.assertEqual(r[-1]["vat_pct_gross_disposable_income"], "5.92")
        self.assertEqual(r[0]["vat_pct_consumption"], "10.5")
        self.assertEqual(r[-1]["vat_pct_consumption"], "11.6")
        for row in r:
            self.assertGreater(Decimal(row["vat_eur_per_household"]), 0)
            self.assertGreater(Decimal(row["vat_pct_gross_disposable_income"]), 0)
            self.assertGreater(Decimal(row["vat_pct_consumption"]), 0)


class TestDistributedProductTax2020to2023(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with PRODUCT.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            cls.columns = reader.fieldnames
            cls.data = list(reader)

    def test_coverage_and_totals(self):
        self.assertEqual(self.columns,
                         ["year", "vingtile", "product_taxes_bn_eur"])
        years = {}
        for row in self.data:
            years.setdefault(int(row["year"]), []).append(row)
            self.assertGreater(Decimal(row["product_taxes_bn_eur"]), 0)
        self.assertEqual(sorted(years), [2020, 2021, 2022, 2023])
        for year, rows in years.items():
            self.assertEqual([int(x["vingtile"]) for x in rows], list(range(1, 21)))
            total = sum(Decimal(r["product_taxes_bn_eur"]) for r in rows)
            expected = Decimal({2020:"273.6",2021:"307.9",2022:"319.0",2023:"318.6"}[year])
            self.assertLessEqual(abs(total - expected), Decimal(".5"))
        self.assertEqual(years[2023][0]["product_taxes_bn_eur"], "8.2")
        self.assertEqual(years[2023][-1]["product_taxes_bn_eur"], "33.3")

    def test_source_and_output_reproduction_helpers(self):
        self.assertEqual(len(SHA256), 64)
        self.assertEqual(HEADER, "year,vingtile,product_taxes_bn_eur\n")
        self.assertTrue(csv_text([(2023,1,Decimal("8.2"))]).endswith("2023,1,8.2\n"))

    def test_scope_does_not_label_product_taxes_as_vat(self):
        self.assertNotIn("vat_", ",".join(self.columns))
        self.assertNotIn("2025", ",".join(self.columns))


if __name__ == "__main__":
    unittest.main()
