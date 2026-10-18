import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/etat_execution_2023_2025.json"


class TestBudgetEtatExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_coverage_and_reconciliation(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual([y["year"] for y in self.data["years"]], [2023, 2024, 2025])
        for year in self.data["years"]:
            self.assertEqual(len(year["missions"]), 33)
            self.assertGreaterEqual(sum(len(m["programs"]) for m in year["missions"]), 129)
            self.assertLessEqual(abs(sum(m["cp_eur"] for m in year["missions"]) - year["spending"]["spent_cp_eur"]), 3)
            refund = next(m for m in year["missions"] if m["name"] == "Remboursements et dégrèvements")
            self.assertEqual(refund["cp_eur"], year["spending"]["refunds_cp_eur"])
            self.assertEqual(year["spending"]["spent_cp_eur"] - refund["cp_eur"],
                             year["spending"]["spent_excluding_refunds_cp_eur"])
            for mission in year["missions"]:
                difference = mission["cp_eur"] - sum(p["cp_eur"] for p in mission["programs"])
                self.assertLessEqual(abs(difference - mission["source_reconciliation_gap_eur"]), 3)
                self.assertEqual(len({p["code"] for p in mission["programs"]}), len(mission["programs"]))
            self.assertEqual(len(year["revenues"]), 4)
            for category in year["revenues"]:
                self.assertLessEqual(abs(category["gross_cash_eur"] -
                    sum(s["gross_cash_eur"] for s in category["sections"])), 3)
                self.assertGreater(len(category["sections"]), 0)

    def test_2024_gross_net_and_2023_source_gap(self):
        years = {y["year"]: y for y in self.data["years"]}
        self.assertEqual(years[2024]["spending"]["spent_cp_eur"], 584981581788)
        self.assertEqual(years[2024]["fiscal_net_2024_eur"], 325679295290)
        self.assertEqual(years[2024]["revenues"][0]["gross_cash_eur"], 467247625870)
        self.assertIsNone(years[2023]["fiscal_net_2024_eur"])
        self.assertIsNone(years[2025]["fiscal_net_2024_eur"])
        gap = [m for m in years[2023]["missions"] if m["source_reconciliation_gap_eur"]]
        self.assertEqual(len(gap), 1)
        self.assertEqual(gap[0]["name"], "Remboursements et dégrèvements")
        self.assertEqual(gap[0]["source_reconciliation_gap_eur"], -83650)

    def test_source_and_page_disclaimers(self):
        html = (ROOT / "etat.html").read_text(encoding="utf-8")
        for phrase in ("ne calculent", "fiscal_net_2024_eur",
                       "source_reconciliation_gap_eur", "CP ouverts",
                       "2023", "2024", "2025", 'href="/atlas-nav.css"'):
            self.assertIn(phrase, html)
        self.assertIn("Source PLRG", (ROOT / "DATA_SOURCES.md").read_text(encoding="utf-8"))
