import csv
from pathlib import Path
import unittest
from scripts.import_jeunes_population import FIELDS,SHA256,SOURCE_ID,extract
ROOT=Path(__file__).resolve().parents[1]
class YouthPopulationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT/'data/jeunes_population_2024_par_age.csv').open(encoding='utf-8',newline='') as stream:
            reader=csv.DictReader(stream);cls.header=reader.fieldnames;cls.rows=list(reader)
    def test_year_age_and_sex_reconciliation(self):
        self.assertEqual(tuple(self.header),FIELDS)
        self.assertEqual([int(x['age']) for x in self.rows],list(range(15,30)))
        for r in self.rows:
            self.assertEqual(r['year'],'2024')
            self.assertEqual(r['territory'],'france')
            self.assertEqual(r['source_id'],SOURCE_ID)
            self.assertEqual(int(r['men'])+int(r['women']),int(r['total']))
    def test_population_denominators_from_single_age_cells(self):
        def n(lo,hi):
            return sum(int(r['total']) for r in self.rows if lo<=int(r['age'])<=hi)
        self.assertEqual(n(18,25),6375226)
        self.assertEqual(n(18,29),9446471)
        self.assertEqual(n(15,24),8209108)
        self.assertEqual(n(18,24),5603770)
    def test_checksum_guard(self):
        self.assertEqual(len(SHA256),64)
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):
            extract(ROOT/'data/jeunes_population_2024_par_age.csv')
    def test_separate_published_employment_populations(self):
        with (ROOT/'data/jeunes_situations_2024_insee.csv').open(encoding='utf-8',newline='') as stream:
            reader=csv.DictReader(stream)
            rows=list(reader)
        self.assertEqual(len(rows),6)
        self.assertEqual({x['age_group'] for x in rows},{'18-20','21-24','25-29'})
        self.assertEqual({x['sex'] for x in rows},{'women','men'})
        for r in rows:
            columns=('study_only','study_and_work','work_only','unemployed','other_inactive')
            total=sum(float(r[k]) for k in columns)
            self.assertLess(abs(total-100),0.11)
            self.assertEqual(r['source_id'],'insee_fps2025_figure2_eec2024')
if __name__=='__main__': unittest.main()
