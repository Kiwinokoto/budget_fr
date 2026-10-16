"""Regression tests for three independent Insee debt tables (28 August 2026)."""
import csv
from decimal import Decimal
from pathlib import Path
import unittest
import zipfile

from scripts import import_debt_bridges as source

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(filename):
    with (DATA / filename).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


class TestDebtBridges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        names = {table: name for table, (_, name) in source.TABLES.items()}
        cls.raw = {table: load(name) for table, name in names.items()}
        cls.by_sector = {
            table: {(int(r["year"]), r["sector"]): r for r in cls.raw[table][1]}
            for table in ("3103", "3104")
        }
        cls.flows = {int(r["year"]): r for r in cls.raw["3105"][1]}

    def test_schema_years_and_unique_sector_keys(self):
        for table, fields, first_year in (("3103",source.NET_FIELDS,1995),
                                          ("3104",source.BRIDGE_FIELDS,1995)):
            header, rows = self.raw[table]
            self.assertEqual(header, list(fields))
            self.assertEqual(len(rows), 31 * len(source.SECTORS))
            self.assertEqual(set(self.by_sector[table]), {
                (y,s) for y in range(first_year,2026) for s in source.SECTORS
            })
        header,rows = self.raw["3105"]
        self.assertEqual(header,list(source.FLOW_FIELDS))
        self.assertEqual(len(rows),17)
        self.assertEqual(set(self.flows),set(range(2009,2026)))

    def test_values_units_and_negative_net_debt(self):
        for table in ("3103","3104","3105"):
            header,rows = self.raw[table]
            for r in rows:
                for field in header:
                    if field in ("year","sector"):
                        continue
                    self.assertTrue(Decimal(r[field]).is_finite(), (table,field,r))
            self.assertEqual(len(source.TABLES[table][0]),64)
        # Net S1314 was negative in some early years: do not clamp to 0.
        self.assertLess(Decimal(self.by_sector["3103"][(1995,"S1314")]["net_debt_bn_eur"]),0)

    def test_net_debt_source_concept(self):
        r = self.by_sector["3103"][(2025,"S13")]
        self.assertEqual(r["net_debt_bn_eur"],"3242.7")
        self.assertEqual(r["other_liquid_assets_bn_eur"],"316.9")
        self.assertEqual(r["net_debt_pct_gdp"],"108.4132")
        # Other liquid assets F511/F52 are reported separately, NOT deducted again.
        self.assertNotEqual(Decimal("3460.1")-Decimal(r["other_liquid_assets_bn_eur"]),
                            Decimal(r["net_debt_bn_eur"]))
        for year in range(1995,2026):
            rows=self.by_sector["3103"]
            q=lambda s: Decimal(rows[(year,s)]["net_debt_bn_eur"])
            self.assertLessEqual(abs(q("S13")-q("S13111")-q("S13112")-q("S1313")-q("S1314")),
                                 source.TOL)

    def test_liabilities_nominal_bridge_and_visible_gap(self):
        rows=self.by_sector["3104"]
        for r in rows.values():
            d=lambda key:Decimal(r[key])
            self.assertLessEqual(abs(
                d("total_liabilities_bn_eur")-d("scope_excluded_bn_eur")
                -d("intrasector_consolidation_bn_eur")
                -d("nominal_value_adjustment_bn_eur")-d("maastricht_bn_eur")), source.TOL)
            self.assertLessEqual(abs(
                d("nominal_value_adjustment_bn_eur")-d("accrued_deposit_interest_bn_eur")
                -d("bond_valuation_adjustment_bn_eur")-d("accrued_loan_interest_bn_eur")
                -d("valuation_breakdown_gap_bn_eur")),source.TOL)
        r=rows[(2025,"S13")]
        self.assertEqual(r["total_liabilities_bn_eur"],"3911.4")
        self.assertEqual(r["maastricht_bn_eur"],"3460.1")
        # Discrepancies in published sub-components are not silently corrected.
        self.assertGreaterEqual(
            abs(Decimal(rows[(2021,"S1311")]["valuation_breakdown_gap_bn_eur"])),Decimal("2.8")
        )

    def test_social_sector_source_discrepancy_documented_not_forced(self):
        # Insee 3.104 itself publishes 293.1 in 2025, unlike 3.102 (292.6).
        self.assertEqual(self.by_sector["3104"][(2025,"S1314")]["maastricht_bn_eur"],"293.1")
        self.assertEqual(self.by_sector["3104"][(2025,"S13")]["maastricht_bn_eur"],"3460.1")
        components=sum(Decimal(self.by_sector["3104"][(2025,s)]["maastricht_bn_eur"])
                       for s in ("S13111","S13112","S1313","S1314"))
        self.assertEqual(components,Decimal("3460.5"))

    def test_flow_bridge_and_true_stock_variation(self):
        r=self.flows[2025]
        self.assertEqual(r["deficit_bn_eur"],"151.6")
        self.assertEqual(r["debt_change_bn_eur"],"154.0")
        for year, rec in self.flows.items():
            d=lambda key: Decimal(rec[key])
            expected=sum((
                d("deficit_bn_eur"),d("financial_assets_acquisition_bn_eur"),
                d("other_financial_liabilities_bn_eur"),d("debt_volume_changes_bn_eur"),
                d("accounts_payable_receivable_bn_eur"),d("statistical_discrepancy_bn_eur")
            ),Decimal(0))
            self.assertLessEqual(abs(d("debt_change_bn_eur")-expected),source.TOL)
            current=Decimal(self.by_sector["3104"][(year,"S13")]["maastricht_bn_eur"])
            previous=Decimal(self.by_sector["3104"][(year-1,"S13")]["maastricht_bn_eur"])
            gap=current-previous-d("debt_change_bn_eur")
            if year == 2014:
                # The two source tables differ by 0.6 Md€ in the pinned XLSX.
                self.assertEqual(gap,Decimal("-0.6"))
            else:
                self.assertLessEqual(abs(gap),source.TOL)

    def test_corrupted_workbook_rejected(self):
        for extractor in source.EXTRACTORS.values():
            with self.assertRaises((ValueError, zipfile.BadZipFile)):
                extractor(b"invalid xlsx")


if __name__=="__main__":
    unittest.main()
