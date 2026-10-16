import csv
from io import BytesIO
from pathlib import Path
import unittest
from zipfile import ZipFile

from scripts.import_insee import FIELDS, extract_rows, format_csv

PATH = Path(__file__).resolve().parents[1] / "data/apu_1960_2025_pct_pib.csv"


class TestPublishedData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with PATH.open(encoding="utf-8", newline="") as file:
            cls.rows = list(csv.DictReader(file))

    def test_coverage(self):
        self.assertEqual([int(r["year"]) for r in self.rows], list(range(1960, 2026)))
        self.assertEqual(list(self.rows[0]), list(FIELDS))

    def test_integrity(self):
        for r in self.rows:
            year = int(r["year"])
            revenue, spending, balance = (float(r[k]) for k in
                ("revenue_pct_gdp", "expenditure_pct_gdp", "balance_pct_gdp"))
            self.assertLessEqual(abs(revenue-spending-balance), 0.06, year)
            self.assertEqual(bool(r["gross_debt_pct_gdp"]), year >= 1978)
            self.assertEqual(bool(r["net_debt_pct_gdp"]), year >= 1995)
            if r["net_debt_pct_gdp"]:
                self.assertLessEqual(float(r["net_debt_pct_gdp"]),
                                     float(r["gross_debt_pct_gdp"]))

    def test_reference_years(self):
        by_year = {int(r["year"]): r for r in self.rows}
        self.assertEqual(by_year[1980]["gross_debt_pct_gdp"], "21.300")
        self.assertEqual(by_year[2019]["revenue_pct_gdp"], "52.953")
        self.assertEqual(by_year[2025]["expenditure_pct_gdp"], "57.308")
        self.assertEqual(by_year[2025]["balance_pct_gdp"], "-5.100")


class TestImporter(unittest.TestCase):
    @staticmethod
    def small_xlsx(bad_balance=False):
        ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        def c(ref, val):
            if isinstance(val, str):
                return '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, val)
            return '<c r="%s"><v>%s</v></c>' % (ref, val)
        def row(n, label, v1, v2):
            return '<row r="%s">%s%s%s%s</row>' % (
                n, c("A%d"%n,label), c("B%d"%n,v1), c("C%d"%n,v2),
                '<c r="D4" t="inlineStr"><is><t></t></is></c>' if n == 4 else '')
        xml = ('<worksheet xmlns="%s"><sheetData>' % ns +
            row(4, "Dépense et recette", "1980", "1981") +
            row(5, "Dépenses", 48, 50) +
            row(6, "    dont dépenses hors éléments imputés1", 46, 48) +
            row(7, "Recettes", 47.6, 48) +
            row(8, "    dont recettes hors éléments imputés1", 45, 46) +
            row(9, "Déficit au sens de Maastricht", -0.4, -1 if bad_balance else -2) +
            row(10, "Dette des administrations publiques (brute)2", 21.3, 22.6) +
            row(11, "Dette nette des administrations publiques3", "nd", "nd") +
            '</sheetData></worksheet>')
        output = BytesIO()
        with ZipFile(output, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", xml.encode("utf-8"))
        return output.getvalue()

    def test_offline(self):
        rows = extract_rows(self.small_xlsx(), expected_years=range(1980,1982))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["revenue_pct_gdp"], "47.600")
        self.assertEqual(rows[0]["net_debt_pct_gdp"], "")
        self.assertEqual(len(format_csv(rows).splitlines()), 3)

    def test_reject_inconsistent_balance(self):
        with self.assertRaisesRegex(ValueError, "Balance consistency"):
            extract_rows(self.small_xlsx(bad_balance=True),
                         expected_years=range(1980,1982))

    def test_reject_changed_years(self):
        with self.assertRaisesRegex(ValueError, "Year coverage changed"):
            extract_rows(self.small_xlsx())


if __name__ == "__main__":
    unittest.main()
