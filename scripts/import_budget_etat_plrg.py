#!/usr/bin/env python3
"""Import executed French State general-budget CP and gross cash receipts (PLRG 2023–2025).

Sources are pinned by SHA-256; all monetary aggregation uses Decimal.
Do not add gross cash receipts to public-administration national-accounting totals.
"""
import argparse
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/etat_execution_2023_2025.json"
SLUGS = {
    2023: "projet-de-loi-relatif-aux-resultats-de-la-gestion-et-portant-approbation-des-comptes-de-lannee-plrg-2023",
    2024: "plrg-2024",
    2025: "projet-de-loi-relatif-aux-resultats-de-la-gestion-et-portant-approbation-des-comptes-de-lannee-plrg-2025",
}
ATTACHMENTS = {
    2023: {
        "cp": ("annexe1_etat_cp_2023_csv", "3729b37c66bce70b1efe08e5e769969f1bdb3302fed8cf3055f74eea8a8270cb"),
        "summary": ("annexe1_etat_ae_cp_2023_csv", "8baa6cc493af545489d4f6c94016b39431c60855cce85a0faa03716980f6838c"),
        "revenue": ("annexe1_etat_recettes_2023_csv", "4a11506f837190c81ab04cd4cf67f3d32f429d7f42d15b41f66163e6e27ca407"),
    },
    2024: {
        "cp": ("annexe1_etat_cp_2024_csv", "2ec0b30f934104ea11c863fc044932c5e260930d0c06e8e05aa0977aa315e90b"),
        "summary": ("annexe1_etat_ae_cp_2024_csv", "5c374be4eb01bf71d007a1c25855d9c81116a09232e3cf653dd166536b8585fa"),
        "revenue": ("annexe1_etat_recettes_csv", "79812995f0429e31f1d60bdf749290ef9d6f003d9c14d018f267cd171d5eb35a"),
    },
    2025: {
        "cp": ("annexe1_etat_cp_2025csv", "6e9e0ddb861a6eb47857b0a481d3e1a293ba8ce96bb9c880431f9d689ce9d5c8"),
        "summary": ("annexe1_etat_ae_cp_2025csv", "ffa348ed5e4a219557884687b84333ac89b3f3bf1e2814a9396404f81e90d7dd"),
        "revenue": ("annexe1_etat_recettes_2025csv", "a5522721ac13758c7ee0bf1b8fcea4f0922ef34673ad5a9af38d5bc94b92ae31"),
    },
}
BASE = "https://data.economie.gouv.fr/api/v2/catalog/datasets/"
CATEGORIES = ("Recettes fiscales", "Recettes non fiscales",
              "Prélèvements sur les recettes de l'État",
              "Fonds de concours et attributions de produits")
SECTION = re.compile(r"^([0-9]{2})\s*[-.]\s*(.+)")
PROGRAM = re.compile(r"^(.+) - ([0-9]{3})$")
EURO = Decimal("1")


def money(value):
    """Whole euros for JSON; retain source cents during all reconciliations."""
    return int(value.quantize(EURO, rounding=ROUND_HALF_UP))


def number(raw):
    value = str(raw or "0").strip().replace("\u00a0", "").replace(" ", "")
    if value in ("", "-", "–"):
        return Decimal(0)
    try:
        n = Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("Invalid monetary figure: " + str(raw)) from exc
    if not n.is_finite():
        raise ValueError("Non-finite monetary figure")
    return n


def rows(blob, delimiter):
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig")), delimiter=delimiter))


def load(year, kind, local_dir=None):
    filename, checksum = ATTACHMENTS[year][kind]
    if local_dir:
        blob = (local_dir / ("plrg_%s_%s.csv" % (year, kind))).read_bytes()
    else:
        url = BASE + SLUGS[year] + "/attachments/" + filename
        with urlopen(url, timeout=35) as stream:
            blob = stream.read()
    if hashlib.sha256(blob).hexdigest() != checksum:
        raise ValueError("PLRG %s %s source SHA-256 changed" % (year, kind))
    return blob


def expenses(year, cp_blob, summary_blob):
    lines = rows(cp_blob, ";")
    summary = rows(summary_blob, ";")
    required = {"Mission", "Programme", "Titre", "LFI", "Total_CP_Ouverts", "Depenses_constatees"}
    if not lines or set(lines[0]) < required:
        raise ValueError("Unexpected CP schema")
    collected = {}
    for line in lines:
        mission = line["Mission"].strip()
        match = PROGRAM.fullmatch(line["Programme"].strip())
        if not mission or not match or not line["Titre"].strip():
            raise ValueError("Incomplete mission/programme/title")
        label, code = match.groups()
        group = collected.setdefault(mission, {})
        item = group.setdefault(code, {"code": code, "name": label,
                                       "cp": Decimal(0), "opened": Decimal(0), "lfi": Decimal(0)})
        if item["name"] != label:
            raise ValueError("Program name mismatch for code " + code)
        for field, column in [("cp", "Depenses_constatees"),
                               ("opened", "Total_CP_Ouverts"), ("lfi", "LFI")]:
            item[field] += number(line[column])
    if len(collected) < 25 or len(summary) != len(collected):
        raise ValueError("Unexpected CP mission coverage")
    published = {}
    for item in summary:
        name = item["Mission"].strip()
        if name in published:
            raise ValueError("Duplicate mission")
        published[name] = number(item["CP_Consommes"])
    if published.keys() != collected.keys():
        raise ValueError("Mismatch in mission coverage")
    result = []
    for mission in sorted(collected):
        sub = collected[mission]
        amount = sum((item["cp"] for item in sub.values()), Decimal(0))
        difference = published[mission] - amount
        # PLRG 2023 summary rounds missions to whole EUR; its refund mission also
        # contains a distinct 83 650.28 EUR mismatch, not an ordinary cent rounding.
        # Keep the published mission total and expose rather than invent a program.
        limit = Decimal("84000") if (year == 2023 and mission == "Remboursements et dégrèvements") else Decimal("2")
        if abs(difference) > limit:
            raise ValueError("PLRG program sums do not reconcile: " + mission)
        result.append({
            "name": mission,
            "cp_eur": money(published[mission]),
            "source_reconciliation_gap_eur": money(difference) if abs(difference) > Decimal("2") else 0,
            "opened_eur": money(sum((x["opened"] for x in sub.values()), Decimal(0))),
            "lfi_eur": money(sum((x["lfi"] for x in sub.values()), Decimal(0))),
            "programs": [
                {"code": x["code"], "name": x["name"], "cp_eur": money(x["cp"]),
                 "opened_eur": money(x["opened"]), "lfi_eur": money(x["lfi"])}
                for x in sorted(sub.values(), key=lambda p: p["code"])
            ],
        })
    if not any(x["name"] == "Remboursements et dégrèvements" for x in result):
        raise ValueError("Missing refund mission")
    total = sum(published.values(), Decimal(0))
    refunds = published["Remboursements et dégrèvements"]
    return result, {"spent_cp_eur": money(total),
                    "spent_excluding_refunds_cp_eur": money(total-refunds),
                    "refunds_cp_eur": money(refunds)}


def revenue(year, blob):
    lines = rows(blob, "," if year == 2024 else ";")
    totals = {category: Decimal(0) for category in CATEGORIES}
    sections = {}
    fiscal_net = None
    if year == 2024:
        levels = {"3": [], "4": []}
        for line in lines:
            level = line.get("Niveau hiérarchique de la ligne")
            if level in levels:
                levels[level].append(line)
        if len(levels["4"]) != 4:
            raise ValueError("Unexpected 2024 category totals")
        for line in levels["4"]:
            category = line["Catégorie"].removesuffix(" (total)")
            if category not in totals:
                raise ValueError("Unexpected 2024 revenue category")
            totals[category] = number(line["Total des recouvrements"])
            if category == CATEGORIES[0]:
                fiscal_net = money(number(line["Total des recettes**"]))
        source_lines = levels["3"]
        numeric_key = "Total des recouvrements"
        category_key = "Catégorie"
    else:
        source_lines = [line for line in lines if line.get("Categorie") in totals]
        numeric_key = "Total_recouvrement" if year == 2023 else "Total_des_recouvrements"
        category_key = "Categorie"
    for line in source_lines:
        category = line[category_key]
        if category not in totals:
            continue
        value = number(line[numeric_key])
        if year != 2024:
            totals[category] += value
        match = SECTION.match(line["Section"])
        if not match:
            if value:
                raise ValueError("Non-classified nonzero receipt")
            continue
        code, label = match.groups()
        label = re.sub(r"\s*\(total\)$", "", label).rstrip("*").strip()
        record = sections.setdefault((category, code), {"code": code, "name": label, "value": Decimal(0)})
        record["value"] += value
    if year == 2024:
        grouped = {category: sum((v["value"] for (c, _), v in sections.items()
                                  if c == category), Decimal(0)) for category in CATEGORIES}
        for category in CATEGORIES:
            if abs(grouped[category] - totals[category]) > Decimal("0.015"):
                raise ValueError("2024 category/subtotal mismatch: " + category)
    if len(sections) < 15 or any(totals[c] == 0 for c in CATEGORIES):
        raise ValueError("Unexpected revenue coverage")
    result = []
    for category in CATEGORIES:
        result.append({
            "name": category,
            "gross_cash_eur": money(totals[category]),
            "sections": [
                {"code": x["code"], "name": x["name"], "gross_cash_eur": money(x["value"])}
                for (c, _), x in sorted(sections.items()) if c == category
            ],
        })
    return result, fiscal_net


def generate(blobs):
    years = []
    for year in sorted(SLUGS):
        missions, totals = expenses(year, blobs[year]["cp"], blobs[year]["summary"])
        receipts, fiscal_net = revenue(year, blobs[year]["revenue"])
        if len(missions) < 25 or sum(len(m["programs"]) for m in missions) < 100:
            raise ValueError("Unexpected mission/program counts")
        years.append({"year": year, "spending": totals, "missions": missions,
                      "revenues": receipts, "fiscal_net_2024_eur": fiscal_net})
    return {"schema_version": 1, "scope": "French State general budget only",
            "accounting": "PLRG executed payment credits and gross cash receipts, EUR nominal",
            "years": years}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, help="Pinned downloaded originals plrg_YEAR_KIND.csv")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    sources = {year: {kind: load(year, kind, args.source_dir)
                      for kind in ("cp", "summary", "revenue")}
               for year in sorted(SLUGS)}
    result = generate(sources)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":"))+"\n",
                           encoding="utf-8")
    print("PLRG execution imported: ", [(y["year"], len(y["missions"]))
                                         for y in result["years"]])


if __name__ == "__main__":
    main()
