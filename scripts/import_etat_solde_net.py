#!/usr/bin/env python3
"""Annual State budget execution from two pinned DGFiP SMB CSV attachments (2013–2025).

Selected December snapshots are cross-checked against the published budget balance.
All figures and all reconciliations remain in Decimal EUR until final JSON export.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import gzip
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUTPUT = Path(__file__).resolve().parents[1] / "data/etat_solde_net_2013_2025.json"
BASE = ("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "situations-mensuelles-budgetaires-series-longues/attachments/")
SOURCES = {
    "2013_2023": (
        "series_longues_smb_dgfip_2013_2023_csv",
        "91a2cba540c6b15c52bb96f3df55a081fa7ce8ba4a30ce4109489079744a1ad7",
        range(2013, 2024),
    ),
    "2024_2025": (
        "serie_longue_smb_dgfip_2024_xxcsv",
        "cf1c3bb08afd11cb966bf6e0d6fcfc00cdc39cf68ddfaec69cef33c5227a773b",
        range(2024, 2026),
    ),
}
# Exact, non-ambiguous source row identities; never sum sub-totals and components.
FIELDS = {
    "solde_eur": ("Solde budgétaire", "Solde budgétaire", "Solde budgétaire"),
    "depenses_bg_nettes_eur": ("Dépenses", "Budget général", "Total dépenses nettes du budget général"),
    "prelevements_recettes_eur": ("Dépenses", "Prélèvements sur recettes", "Total prélèvements sur recettes"),
    "recettes_bg_nettes_eur": ("Recettes", "Budget général", "Total recettes nettes du budget général"),
    "recettes_fiscales_nettes_eur": ("Recettes", "Budget général", "Total recettes fiscales"),
    "recettes_non_fiscales_eur": ("Recettes", "Budget général", "Total recettes non fiscales"),
    "solde_comptes_speciaux_eur": ("Soldes", "Comptes spéciaux", "Solde des comptes spéciaux"),
    "solde_budgets_annexes_eur": ("Soldes", "Budgets annexes", "Solde des Budgets annexes"),
    "fonds_concours_eur": ("Recettes", "Budget général", "Fonds de concours et attribution de produits"),
}
MAX_EUR_RESIDUAL = Decimal("0.01")


def decimal_value(value):
    if value is None or not str(value).strip():
        raise ValueError("Missing official monetary amount")
    try:
        number = Decimal(str(value).strip().replace("\u00a0", "").replace(" ", "").replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("Invalid monetary amount: " + str(value)) from exc
    if not number.is_finite():
        raise ValueError("Non-finite amount")
    return number


def load_source(key, directory=None):
    file_id, expected_sha, _ = SOURCES[key]
    if directory is not None:
        raw = (directory / ("smb_" + key + ".csv")).read_bytes()
    else:
        request = Request(BASE + file_id, headers={"Accept-Encoding": "identity"})
        with urlopen(request, timeout=40) as response:
            raw = response.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        raise ValueError("Official SMB attachment changed for %s: %s" % (key, actual_sha))
    return raw


def collect(blob, expected_years):
    if not blob.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise ValueError("Unexpected SMB CSV encoding (expected UTF-16)")
    table = list(csv.DictReader(io.StringIO(blob.decode("utf-16")), delimiter=";"))
    if not table or not set(("Catégorie", "Sous-catégorie", "Ligne d'information")) <= set(table[0]):
        raise ValueError("Unexpected SMB columns")
    lookup = {}
    for row in table:
        cat, sub, label = (row.get(k, "").strip() for k in
                           ("Catégorie", "Sous-catégorie", "Ligne d'information"))
        if not any((cat, sub, label) == target for target in FIELDS.values()):
            continue
        key = (cat, sub, label)
        if key in lookup:
            raise ValueError("Duplicate official budget line: " + str(key))
        lookup[key] = row
    if set(lookup) != set(FIELDS.values()):
        raise ValueError("Missing mandatory budget line(s): " +
                         str(set(FIELDS.values()) - set(lookup)))
    result = []
    for year in expected_years:
        column = "31/12/%d" % year
        if column not in table[0]:
            raise ValueError("Missing year column: " + column)
        amounts = {field: decimal_value(lookup[target].get(column))
                   for field, target in FIELDS.items()}
        income_gap = (amounts["recettes_bg_nettes_eur"] -
                      amounts["recettes_fiscales_nettes_eur"] -
                      amounts["recettes_non_fiscales_eur"])
        # "Dépenses" and prélèvements are positive, deducted below.
        # Fonds de concours and the net balances of specials/annexes are added once.
        reconstructed = (amounts["recettes_bg_nettes_eur"] -
                         amounts["depenses_bg_nettes_eur"] -
                         amounts["prelevements_recettes_eur"] +
                         amounts["solde_comptes_speciaux_eur"] +
                         amounts["solde_budgets_annexes_eur"] +
                         amounts["fonds_concours_eur"])
        balance_gap = amounts["solde_eur"] - reconstructed
        if abs(income_gap) > MAX_EUR_RESIDUAL or abs(balance_gap) > MAX_EUR_RESIDUAL:
            raise ValueError("State budget reconciliation failed in %s: %s / %s EUR" %
                             (year, income_gap, balance_gap))
        # Amounts stored as integer EUR; sub-euro reconciliation occurs above.
        integer_eur = lambda n: int(n.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        result.append({"year": year, **{key: integer_eur(v) for key, v in amounts.items()}})
    return result


def generate(source_blobs):
    all_years = []
    for key, (_, _, years) in SOURCES.items():
        all_years += collect(source_blobs[key], years)
    if [row["year"] for row in all_years] != list(range(2013, 2026)):
        raise ValueError("Unexpected period or year coverage")
    return {
        "schema_version": 1,
        "scope": "Etat, execution budgetaire SMB DGFiP; includes special accounts and annex budget balances",
        "unit": "EUR courants, integer EUR rounded after exact Decimal verification",
        "years": all_years,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Directory containing smb_2013_2023.csv and smb_2024_2025.csv")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = generate({key: load_source(key, args.source_dir) for key in SOURCES})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf-8")
    print("SMB annual State budget: %d audited years, %d–%d" %
          (len(result["years"]), result["years"][0]["year"], result["years"][-1]["year"]))


if __name__ == "__main__":
    main()
