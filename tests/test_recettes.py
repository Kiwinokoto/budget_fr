import csv
from decimal import Decimal
from io import BytesIO
from pathlib import Path
import unittest
from zipfile import ZipFile

from scripts.import_recettes import FIELDS, POSITIVE, SERIES, extract_rows, format_csv

CSV = Path(__file__).resolve().parents[1] / "data/recettes_1995_2025_bn_eur.csv"


class TestRevenueData(unittest.TestCase):
    def test_years_and_reconciliation(self):
        with CSV.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, list(FIELDS))
            rows = list(reader)
        self.assertEqual([int(r["year"]) for r in rows], list(range(1995, 2026)))
        for row in rows:
            values = {k: Decimal(v) for k, v in row.items() if k != "year"}
            subtotal = sum(values[k] for k in POSITIVE)
            self.assertLessEqual(abs(subtotal + values["uncollectable_bn_eur"] +
                values["tax_credits_bn_eur"] - values["levies_bn_eur"]), Decimal("0.005"))
            self.assertLessEqual(abs(subtotal + values["social_imputed_bn_eur"] -
                values["gross_taxes_social_bn_eur"]), Decimal("0.005"))
            self.assertLess(values["uncollectable_bn_eur"], 0)
            self.assertLessEqual(values["tax_credits_bn_eur"], 0)
            self.assertGreater(values["levies_pct_gdp"], 0)
        self.assertEqual(rows[-1]["vat_bn_eur"], "208.821")
        self.assertEqual(rows[-1]["levies_bn_eur"], "1305.067")
        self.assertEqual(rows[-1]["csg_bn_eur"], "156.583")
        self.assertEqual(rows[0]["year"], "1995")

    @staticmethod
    def mini_source(bad=False):
        ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        def cell(ref, value):
            if isinstance(value, str):
                return '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, value.replace("&", "&amp;"))
            return '<c r="%s"><v>%s</v></c>' % (ref, value)
        def row(n, vals):
            return '<row r="%d">%s</row>' % (n,"".join(cell("B%d"%n if i == 0 else
                ("%s%d" % ("C" if i == 1 else "D", n)),v)
                for i,v in enumerate(vals)))
        xml = ['<worksheet xmlns="%s"><sheetData>' % ns,
               '<row r="3">%s%s%s</row>' % (cell("C3", "1995"),cell("D3", "1996"),cell("E3", ""))]
        numbers = dict((field, 1 if field in POSITIVE else 0) for field in FIELDS[1:])
        numbers.update({"levies_bn_eur": 9, "levies_pct_gdp": 35,
                        "gross_taxes_social_bn_eur": 9,
                        "social_imputed_bn_eur": 0, "uncollectable_bn_eur": 0,
                        "tax_credits_bn_eur": 0, "income_bn_eur": 4,
                        "irpp_before_credits_bn_eur": 1, "is_before_credits_bn_eur": 1,
                        "csg_bn_eur": 1, "crds_bn_eur": 1})
        numbers["levies_bn_eur"] = 12 if bad else 12  # recompute from positive
        # Nine independent positives: eight at 1 and income at 4 = 12.
        numbers["gross_taxes_social_bn_eur"] = 12
        for field, n, label in SERIES:
            xml.append(row(n,[label,numbers[field],numbers[field]]))
        xml.append('</sheetData></worksheet>')
        out=BytesIO()
        with ZipFile(out,"w") as archive:
            archive.writestr("xl/worksheets/sheet1.xml","".join(xml))
        return out.getvalue()

    def test_parser_offline(self):
        parsed=extract_rows(self.mini_source(),expected_years=range(1995,1997))
        self.assertEqual(len(parsed),2)
        self.assertEqual(len(format_csv(parsed).splitlines()),3)

    def test_reject_wrong_header(self):
        with self.assertRaisesRegex(ValueError,"year coverage"):
            extract_rows(self.mini_source())

    def test_reject_changed_source_label(self):
        data=self.mini_source()
        # The importer must fail rather than infer which series a renamed row means.
        with ZipFile(BytesIO(data)) as archive:
            xml=archive.read("xl/worksheets/sheet1.xml")
        xml=xml.replace(b'Taxe sur la valeur ajout',b'Fausse sur la valeur ajout',1)
        out=BytesIO()
        with ZipFile(out,"w") as archive:
            archive.writestr("xl/worksheets/sheet1.xml",xml)
        with self.assertRaisesRegex(ValueError,"label changed"):
            extract_rows(out.getvalue(),expected_years=range(1995,1997))


if __name__ == "__main__":
    unittest.main()
