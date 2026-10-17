import csv
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class TestApprentissageResultats(unittest.TestCase):
    def test_four_exclusive_source_observations(self):
        with (ROOT/"data/apprentissage_parcours_2024_inserjeunes.csv").open(encoding="utf-8",newline="") as f:
            values=list(csv.DictReader(f))
        self.assertEqual(len(values),4)
        self.assertEqual([(r["indicator"],r["pathway"],int(r["percent"])) for r in values],[
            ("continue_studies","apprenticeship",39),
            ("continue_studies","school_pathway",54),
            ("salaried_employment_6m","apprenticeship",62),
            ("salaried_employment_6m","school_pathway",41),
        ])
        self.assertEqual([r["denominator"] for r in values],["final_year_enrolled"]*2+["non_continuing_leavers"]*2)
        self.assertEqual(set(r["school_year"] for r in values),{"2023-2024"})
        self.assertEqual(set(r["observation"] for r in values),{"next_school_year","2025-01"})
        self.assertEqual(set(r["source_id"] for r in values),{"dares_depp_2025_apprentices_2024","depp_2025_school_pathway_2024"})
    def test_static_page_labels_and_limits(self):
        html=(ROOT/"apprentissage-resultats.html").read_text(encoding="utf-8")
        for value in ("39 %","54 %","62 %","41 %","32 %","18 %","67 %","28 %","80 500","15 594"):
            self.assertIn(value,html)
        self.assertIn("inscrits en dernière année",html)
        self.assertIn("sortants ne poursuivant pas",html)
        self.assertIn("réduction relative de 19 %",html)
        self.assertIn("ne constituent pas une estimation d'impact",html)
        self.assertIn('href="/atlas-nav.css"',html)
        self.assertIn('href="/apprentissage.html"',html)
    def test_provenance_links_and_no_double_counting(self):
        source=(ROOT/"APPRENTISSAGE_RESULTATS_SOURCES.md").read_text()
        self.assertIn("21 points d'écart d'emploi ne valent pas 21 points",source)
        self.assertIn("Aucun classeur brut",source)
        self.assertIn("32 %",source)
        for name in ("apprentissage.html","apprentissage-contexte.html"):
            text=(ROOT/name).read_text()
            self.assertIn('href="/apprentissage-resultats.html"',text)
        self.assertIn("apprentissage-resultats.html",(ROOT/"deploy/README.md").read_text())
        self.assertIn("apprentissage-resultats.html",(ROOT/"ROADMAP.md").read_text())
