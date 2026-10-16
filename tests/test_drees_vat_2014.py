import csv
from decimal import Decimal
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'data/tva_part_deciles_ines_2014.csv'
EXPECTED = [Decimal(x) for x in ('4.3','6.3','7.2','8.0','8.9','9.8','11.0','12.0','14.0','18.5')]

class TestDreesInes2014(unittest.TestCase):
    def test_exact_table_16(self):
        with DATA.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, ['decile','vat_share_pct'])
            rows = list(reader)
        self.assertEqual([int(row['decile']) for row in rows], list(range(1,11)))
        actual=[Decimal(row['vat_share_pct']) for row in rows]
        self.assertEqual(actual, EXPECTED)
        self.assertEqual(sum(actual), Decimal('100.0'))
        self.assertTrue(all(Decimal('0') < x < Decimal('100') for x in actual))

if __name__ == '__main__':
    unittest.main()
