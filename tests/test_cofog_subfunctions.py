import csv
import json
from decimal import Decimal
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT / "data/cofog_1995_2024_bn_eur.csv"
DETAIL = ROOT / "data/cofog_subfunctions_1995_2024.json"


class TestCofogSubfunctions(unittest.TestCase):
    def test_second_level_reconciliation_every_year(self):
        data = json.loads(DETAIL.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["years"], list(range(1995, 2025)))
        self.assertEqual([category["code"] for category in data["categories"]],
                         ["gf%02d" % i for i in range(1, 11)])
        self.assertEqual(sum(len(item["children"]) for item in data["categories"]), 69)
        with TOP.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        for index, year in enumerate(data["years"]):
            self.assertEqual(int(rows[index]["year"]), year)
            for category in data["categories"]:
                prefix = category["code"]
                children = category["children"]
                self.assertEqual(len({child["code"] for child in children}), len(children))
                amounts = []
                for child in children:
                    self.assertTrue(child["code"].startswith(prefix))
                    self.assertEqual(len(child["code"]), 6)
                    self.assertTrue(child["label"].strip())
                    self.assertEqual(len(child["values"]), 30)
                    value = Decimal(str(child["values"][index]))
                    self.assertGreaterEqual(value, 0)
                    amounts.append(value)
                self.assertLessEqual(
                    abs(sum(amounts) - Decimal(rows[index][prefix])),
                    Decimal("0.015"),
                    (prefix, year),
                )

    def test_social_protection_2024_and_units(self):
        data = json.loads(DETAIL.read_text(encoding="utf-8"))
        social = next(category for category in data["categories"] if category["code"] == "gf10")
        values = {item["code"]: item["values"][-1] for item in social["children"]}
        self.assertEqual(values["gf1002"], 391.954)
        self.assertEqual(values["gf1001"], 83.899)
        self.assertEqual(values["gf1004"], 66.711)
        self.assertAlmostEqual(sum(values.values()), 693.029, delta=0.015)
        from scripts.import_cofog import SOURCE_SHA256
        self.assertEqual(SOURCE_SHA256, "ce36c71eafebdcbd941ef5cb74f10e79734fa4e1cc0dc1e97d84e321412c5ce5")
