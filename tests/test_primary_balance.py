import csv
from decimal import Decimal
from pathlib import Path
import unittest

from scripts import import_primary_balance as primary

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data/solde_primaire_apu_1959_2025_bn_eur.csv"
INTEREST = ROOT / "data/interets_apu_1959_2025_bn_eur.csv"


class TestPrimaryBalance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CSV.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            cls.header = reader.fieldnames
            cls.rows = list(reader)

    def test_all_years_and_columns(self):
        self.assertEqual(self.header, primary.HEADER.strip().split(","))
        self.assertEqual([int(r["year"]) for r in self.rows], list(range(1959, 2026)))
        for record in self.rows:
            for key in self.header[1:]:
                self.assertTrue(Decimal(record[key]).is_finite())

    def test_accounting_identities_and_interest_match(self):
        with INTEREST.open(newline="", encoding="utf-8") as stream:
            existing = list(csv.DictReader(stream))
        for balance, interest in zip(self.rows, existing):
            self.assertEqual(balance["year"], interest["year"])
            self.assertEqual(balance["interest_d41_bn_eur"], interest["interest_d41_bn_eur"])
            self.assertEqual(balance["interest_d41g_bn_eur"], interest["interest_ex_fisim_bn_eur"])
            self.assertEqual(balance["total_expenditure_bn_eur"], interest["total_expenditure_bn_eur"])
            b9 = Decimal(balance["balance_b9_bn_eur"])
            for key_interest, key_primary in (
                ("interest_d41_bn_eur", "primary_d41_bn_eur"),
                ("interest_d41g_bn_eur", "primary_d41g_bn_eur"),
            ):
                self.assertEqual(b9 + Decimal(balance[key_interest]),
                                 Decimal(balance[key_primary]))

    def test_2025_exact_rounded_source_and_1980(self):
        end = self.rows[-1]
        self.assertEqual(end["balance_b9_bn_eur"], "-151.5920")
        self.assertEqual(end["interest_d41_bn_eur"], "65.7209")
        self.assertEqual(end["interest_d41g_bn_eur"], "64.6519")
        self.assertEqual(end["primary_d41_bn_eur"], "-85.8711")
        self.assertEqual(end["primary_d41g_bn_eur"], "-86.9401")
        self.assertEqual(self.rows[21]["primary_d41_bn_eur"], "3.5788")
        self.assertEqual(self.rows[50]["year"], "2009")
        self.assertEqual(self.rows[50]["primary_d41_bn_eur"], "-93.5524")

    def test_positive_and_negative_primary_balances(self):
        signs = {Decimal(r["primary_d41_bn_eur"]) > 0 for r in self.rows}
        self.assertEqual(signs, {True, False})

    def test_formatter_and_source_scope(self):
        self.assertEqual(len(primary.source.SHA256), 64)
        self.assertEqual(primary.REVENUE_LABEL, "Total des recettes")
        self.assertEqual(primary.BALANCE_LABEL,
                         "Capacité (+) ou besoin (-) de financement (B9NF)")
        example = (2025, Decimal("-151.5920"), Decimal("65.7209"),
                   Decimal("64.6519"), Decimal("-85.8711"),
                   Decimal("-86.9401"), Decimal("1714.1117"))
        self.assertEqual(primary.format_csv([example]),
                         primary.HEADER +
                         "2025,-151.5920,65.7209,64.6519,-85.8711,-86.9401,1714.1117\n")


if __name__ == "__main__":
    unittest.main()
