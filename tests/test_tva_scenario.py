import csv
from decimal import Decimal
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'data/tva_choc_deciles_insee_2019.csv'
FIELDS = ('decile','income_before_pp','direct_tax_pp','indirect_tax_pp',
          'benefits_pp','rent_pp','net_living_standard_pct')


class TestVatScenario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA.open(encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            cls.names = reader.fieldnames
            cls.data = list(reader)

    def test_source_schema_and_deciles(self):
        self.assertEqual(self.names, list(FIELDS))
        self.assertEqual([int(row['decile']) for row in self.data], list(range(1, 11)))

    def test_transcription_spot_checks(self):
        # Insee Analyses 43, figure 2 (2019), scenario +3pp standard VAT rate.
        first, last = self.data[0], self.data[-1]
        self.assertEqual(first['indirect_tax_pp'], '-2.8')
        self.assertEqual(last['indirect_tax_pp'], '-1.0')
        self.assertEqual(first['net_living_standard_pct'], '-1.4')
        self.assertEqual(last['net_living_standard_pct'], '-0.5')
        self.assertEqual(self.data[1]['benefits_pp'], '0.6')
        self.assertEqual(self.data[8]['direct_tax_pp'], '-0.1')

    def test_partial_components_rounding_and_sign(self):
        for row in self.data:
            numbers = {k: Decimal(row[k]) for k in FIELDS[1:]}
            components = sum(numbers[k] for k in (
                'income_before_pp','direct_tax_pp','indirect_tax_pp','benefits_pp','rent_pp'
            ))
            # Official published components individually rounded to 0.1pp.
            self.assertLessEqual(abs(components-numbers['net_living_standard_pct']),
                                 Decimal('0.15'))
            self.assertLess(numbers['indirect_tax_pp'], 0)
            self.assertLess(numbers['net_living_standard_pct'], 0)

    def test_no_mixup_with_yearly_vat_series(self):
        self.assertNotIn('year', self.names)
        self.assertNotIn('vat_bn_eur', self.names)


if __name__ == '__main__':
    unittest.main()
