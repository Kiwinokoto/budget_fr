import csv
from decimal import Decimal
import io
import json
from pathlib import Path
import unittest

from scripts.import_etat_solde_net import FIELDS, SOURCES, collect, decimal_value

ROOT = Path(__file__).resolve().parents[1]


class TestEtatSoldeNet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data/etat_solde_net_2013_2025.json").read_text(encoding="utf-8"))

    def test_official_years_and_reconciliation(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual([r["year"] for r in self.data["years"]], list(range(2013, 2026)))
        self.assertEqual(len(SOURCES), 2)
        for y in self.data["years"]:
            self.assertLessEqual(abs(
                y["recettes_bg_nettes_eur"] -
                y["recettes_fiscales_nettes_eur"] -
                y["recettes_non_fiscales_eur"]), 2)
            calculated = (
                y["recettes_bg_nettes_eur"] - y["depenses_bg_nettes_eur"]
                - y["prelevements_recettes_eur"]
                + y["solde_comptes_speciaux_eur"]
                + y["solde_budgets_annexes_eur"] + y["fonds_concours_eur"]
            )
            self.assertLessEqual(abs(calculated - y["solde_eur"]), 4, y["year"])
        latest = self.data["years"][-1]
        self.assertEqual(latest["solde_eur"], -124205673502)
        self.assertEqual(latest["recettes_fiscales_nettes_eur"], 356397925510)

    def test_strict_parser_rejects_missing_and_bad_numbers(self):
        with self.assertRaises(ValueError):
            decimal_value("")
        with self.assertRaises(ValueError):
            decimal_value("NaN")
        with self.assertRaises(ValueError):
            decimal_value("not-a-number")
        self.assertEqual(decimal_value("12 456,07"), Decimal("12456.07"))
        source = []
        for key, target in FIELDS.items():
            cat, sub, label = target
            source.append([0, "Sous-total", cat, sub, label, "100"])
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["Niveau hiérarchique", "Niveau hiérarchique de la ligne",
                         "Catégorie", "Sous-catégorie", "Ligne d'information", "31/12/2013"])
        writer.writerows(source)
        with self.assertRaisesRegex(ValueError, "reconciliation failed"):
            collect(output.getvalue().encode("utf-16"), [2013])
        with self.assertRaisesRegex(ValueError, "Missing year"):
            collect(output.getvalue().encode("utf-16"), [2014])

    def test_page_explains_no_synthetic_plrg_history(self):
        html = (ROOT / "etat.html").read_text(encoding="utf-8")
        self.assertIn('id="balance-chart"', html)
        self.assertIn('id="balance-year"', html)
        self.assertIn("2013–2022 n'a pas encore été audité", html)
        self.assertIn("2013–2025", html)


if __name__ == "__main__":
    unittest.main()
