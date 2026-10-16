#!/usr/bin/env python3
"""Compute a transparent primary balance for France's consolidated APU (S13).

Same Insee 3.201 vintage and workbook for net lending/borrowing (B9NF),
interest D41, alternate interest before FISIM correction (D41G), and spending.
Primary balance is DERIVED, not a separately published source row.
No nominal GDP or interest-income netting is inferred.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
from pathlib import Path
import urllib.request

if __package__:
    from . import import_interest as source
else:
    import import_interest as source

OUTPUT = Path(__file__).resolve().parents[1] / "data/solde_primaire_apu_1959_2025_bn_eur.csv"
HEADER = ("year,balance_b9_bn_eur,interest_d41_bn_eur,"
          "interest_d41g_bn_eur,primary_d41_bn_eur,"
          "primary_d41g_bn_eur,total_expenditure_bn_eur\n")
PRECISION = Decimal("0.0001")
REVENUE_LABEL = "Total des recettes"
BALANCE_LABEL = "Capacité (+) ou besoin (-) de financement (B9NF)"


def extract(blob):
    # Insee interest importer also checks the 67 years, rows and source labels.
    interests = source.extract(blob)
    rows = source.parse_rows(blob, extra_rows=(58, 66))
    if rows[58].get("B", "").strip() != REVENUE_LABEL:
        raise ValueError("Insee revenue label changed")
    if rows[66].get("B", "").strip() != BALANCE_LABEL:
        raise ValueError("Insee financing-balance label changed")

    result = []
    for year, d41, d41g, total_expenditure in interests:
        column = source.column(year - 1959 + 2)
        vals = []
        for row_index in (58, 66):
            try:
                raw = rows[row_index][column]
                value = Decimal(raw)
            except (KeyError, InvalidOperation, TypeError) as exc:
                raise ValueError("Invalid Insee B9NF/revenue value: %d" % year) from exc
            if not value.is_finite():
                raise ValueError("Non-finite input value: %d" % year)
            vals.append(value.quantize(PRECISION))
        revenue, balance = vals
        d41, d41g, total_expenditure = (
            value.quantize(PRECISION)
            for value in (d41, d41g, total_expenditure)
        )
        # B9NF = total revenue minus total expenditure. After independent
        # rounding to 0.0001 billion, a 0.0001 tolerance is appropriate.
        if abs(revenue - total_expenditure - balance) > PRECISION:
            raise ValueError("Insee B9NF does not reconcile: %d" % year)
        result.append((year, balance, d41, d41g,
                       balance + d41, balance + d41g, total_expenditure))
    return result


def format_csv(records):
    return HEADER + "".join(
        "%d,%s\n" % (
            year, ",".join(format(value, ".4f") for value in amounts)
        )
        for year, *amounts in records
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--allow-source-change", action="store_true")
    args = parser.parse_args()
    if args.xlsx:
        blob = args.xlsx.read_bytes()
    else:
        with urllib.request.urlopen(source.URL, timeout=35) as response:
            blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != source.SHA256 and not args.allow_source_change:
        raise SystemExit("Insee 3.201 source SHA-256 changed (%s); audit first" % digest)
    data = format_csv(extract(blob))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(data, encoding="utf-8")
    print("B9NF/D41/D41G SHA256=%s; 1959–2025; output=%s" % (digest, args.output))


if __name__ == "__main__":
    main()
