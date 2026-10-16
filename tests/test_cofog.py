import csv
from decimal import Decimal
from io import BytesIO
from pathlib import Path
import unittest
from zipfile import ZipFile

from scripts.import_cofog import CODES, FIELDS, TOTAL_LABEL, extract_rows, format_csv

FILE = Path(__file__).resolve().parents[1] / "data/cofog_1995_2024_bn_eur.csv"


class TestCofogDataset(unittest.TestCase):
    def test_coverage_categories_and_sum(self):
        with FILE.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(reader.fieldnames, list(FIELDS))
            data = list(reader)
        self.assertEqual([int(row["year"]) for row in data], list(range(1995, 2025)))
        for row in data:
            vals = [Decimal(row[field]) for field in FIELDS[1:]]
            self.assertLessEqual(abs(vals[0] - sum(vals[1:])), Decimal("0.015"))
            self.assertTrue(all(value >= 0 for value in vals))
        self.assertEqual(data[0]["total_bn_eur"], "680.371")
        self.assertEqual(data[-1]["total_bn_eur"], "1671.794")
        self.assertEqual(data[-1]["gf10"], "693.029")

    @staticmethod
    def mini_workbook(bad_total=False):
        ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

        def cell(ref, val):
            if isinstance(val, str):
                return '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, val)
            return '<c r="%s"><v>%s</v></c>' % (ref, val)

        def row(number, label, code, v1, v2):
            return '<row r="%d">%s%s%s%s%s%s%s</row>' % (
                number, cell("A%d" % number, "OTE"),
                cell("B%d" % number, label),
                cell("C%d" % number, code),
                cell("D%d" % number, code),
                cell("E%d" % number, v1),
                cell("F%d" % number, v2),
                cell("G%d" % number, ""))

        header = ('<row r="4">' + cell("E4", "1995") + cell("F4", "1996")
                  + cell("G4", "") + '</row>')
        values = [row(6, TOTAL_LABEL, "_Z", 11 if bad_total else 10, 20)]
        values += [row(7 + k, TOTAL_LABEL, code, 1, 2)
                   for k, code in enumerate(CODES[1:])]
        xml = '<worksheet xmlns="%s"><sheetData>%s%s</sheetData></worksheet>' % (
            ns, header, "".join(values))
        out = BytesIO()
        with ZipFile(out, "w") as archive:
            archive.writestr("xl/worksheets/sheet1.xml", xml)
        return out.getvalue()

    def test_offline_parsing(self):
        rows = extract_rows(self.mini_workbook(), expected_years=range(1995, 1997))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["gf01"], "1.000")
        self.assertEqual(len(format_csv(rows).splitlines()), 3)

    def test_reject_nonreconciling_total(self):
        with self.assertRaisesRegex(ValueError, "reconcile"):
            extract_rows(self.mini_workbook(bad_total=True),
                         expected_years=range(1995, 1997))

    def test_reject_changed_years(self):
        with self.assertRaisesRegex(ValueError, "year coverage"):
            extract_rows(self.mini_workbook())


if __name__ == "__main__":
    unittest.main()
