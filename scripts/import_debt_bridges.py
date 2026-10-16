#!/usr/bin/env python3
"""Three separately defined Insee public-debt datasets (base 2020, 28 Aug 2026).

3.103 net debt + OTHER liquid assets: year-end stocks (1995-2025).
3.104 national-accounts liabilities -> nominal consolidated Maastricht stock.
3.105 deficit -> ANNUAL change in Maastricht stock (2009-2025).
Units for financial amounts: billion current EUR; net debt also % of GDP.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import io
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
TABLES = {
    "3103": ("4990cee1dddc3a8d68349f2c3e1918272a67ff777cf1b8e517a9ff2d26fdd804", "dette_nette_apu_1995_2025.csv"),
    "3104": ("b3f8fcb59c927c67fe753b79ad6292f01e488f5c66a9f2ea02f766a7306ffc19", "dette_passifs_maastricht_1995_2025.csv"),
    "3105": ("964ccff6ff8ca50d00b8031b337bfcf94fa7e92056946d73e3a1594d36745234", "dette_deficit_variation_2009_2025.csv"),
}
SECTORS = ("S13", "S1311", "S13111", "S13112", "S1313", "S1314")
NET_FIELDS = ("year", "sector", "net_debt_bn_eur", "net_debt_pct_gdp", "other_liquid_assets_bn_eur")
BRIDGE_FIELDS = ("year", "sector", "total_liabilities_bn_eur", "scope_excluded_bn_eur",
    "payables_derivatives_bn_eur", "guarantee_deposits_bn_eur",
    "intrasector_consolidation_bn_eur", "consolidated_deposits_bn_eur",
    "consolidated_securities_bn_eur", "consolidated_loans_bn_eur",
    "nominal_value_adjustment_bn_eur", "accrued_deposit_interest_bn_eur",
    "bond_valuation_adjustment_bn_eur", "accrued_loan_interest_bn_eur",
    "maastricht_bn_eur", "valuation_breakdown_gap_bn_eur")
FLOW_FIELDS = ("year", "deficit_bn_eur", "financial_assets_acquisition_bn_eur",
    "asset_deposits_bn_eur", "asset_securities_bn_eur", "asset_loans_bn_eur",
    "asset_equity_bn_eur", "asset_derivatives_bn_eur", "asset_insurance_bn_eur",
    "other_financial_liabilities_bn_eur", "accrued_interest_liabilities_bn_eur",
    "other_liabilities_bn_eur", "debt_volume_changes_bn_eur",
    "reclassifications_bn_eur", "fx_valuation_bn_eur", "buyback_gain_loss_bn_eur",
    "accounts_payable_receivable_bn_eur", "statistical_discrepancy_bn_eur",
    "debt_change_bn_eur")
BRIDGE_OFFSETS = (2, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 18)
FLOW_ROWS = (5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 24, 26, 28)
TOL = Decimal("0.35")


def column(index):
    value = ""
    while index:
        index, rem = divmod(index - 1, 26)
        value = chr(65 + rem) + value
    return value


def parse_grid(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            shared = ["".join(q.text or "" for q in item.iter(NS + "t"))
                      for item in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
        rows = {}
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        for r in sheet.findall(".//" + NS + "sheetData/" + NS + "row"):
            cells = {}
            for c in r.findall(NS + "c"):
                ref = re.match(r"^[A-Z]+", c.attrib["r"])
                if not ref:
                    raise ValueError("Invalid source cell reference")
                v, inline = c.find(NS + "v"), c.find(NS + "is")
                raw = (v.text or "") if v is not None else (
                    "".join(q.text or "" for q in inline.iter(NS + "t"))
                    if inline is not None else "")
                if c.get("t") == "s" and raw:
                    raw = shared[int(raw)]
                cells[ref.group()] = raw
            rows[int(r.attrib["r"])] = cells
        return rows


def cell(rows, row, col, signed=False):
    try:
        v = Decimal(rows[row][col])
    except (KeyError, InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid or missing {col}{row}") from exc
    if not v.is_finite() or (v < 0 and not signed):
        raise ValueError(f"Invalid sign/number at {col}{row}")
    return v


def year_cols(rows, row, first, last):
    expected = {column(3+i): str(year) for i, year in enumerate(range(first, last+1))}
    if {k:v for k,v in rows[row].items() if k not in ("A","B") and v} != expected:
        raise ValueError("Source years or layout changed")
    return [(year, column(3+i)) for i,year in enumerate(range(first,last+1))]


def require(rows, row, col, text):
    if text.casefold() not in rows.get(row, {}).get(col, "").casefold():
        raise ValueError(f"Unexpected Insee label {col}{row}: expected {text}")


def equal(label, a, b, tol=TOL):
    if abs(a-b) > tol:
        raise ValueError(f"Cannot reconcile {label}: {a} != {b}")


def extract_3103(blob):
    rows = parse_grid(blob)
    for row,col,label in ((1,"A","3.103 Dette nette"),(5,"B","Dette nette en milliards"),
                          (13,"B","Dette nette en % du PIB"),(21,"B","Autres actifs liquides"),
                          (33,"B","actifs exigibles")):
        require(rows,row,col,label)
    years = year_cols(rows, 3, 1995, 2025)
    for j,sector in enumerate(SECTORS):
        for first in (6,14,22):
            require(rows,first+j,"B",sector+" - ")
    records=[]
    for year,col in years:
        values={}
        for j,sector in enumerate(SECTORS):
            net=cell(rows,6+j,col,signed=True)
            pct=cell(rows,14+j,col,signed=True)
            extra=cell(rows,22+j,col)
            values[sector]=net
            records.append((year,sector,net,pct,extra))
        equal(f"net S13 sub-sector sum {year}",values["S13"],
              sum(values[s] for s in ("S13111","S13112","S1313","S1314")))
        equal(f"net central sub-sector sum {year}",values["S1311"],
              values["S13111"]+values["S13112"])
    if next(r for r in records if r[:2]==(2025,"S13"))[2].quantize(Decimal(".1"))!=Decimal("3242.7"):
        raise ValueError("3.103 audited 2025 anchor changed")
    return NET_FIELDS, records


def extract_3104(blob):
    rows=parse_grid(blob)
    require(rows,1,"A","3.104 Passage du total des passifs")
    years=year_cols(rows,3,1995,2025)
    starts=(5,25,45,65,85,105)
    for first,sector in zip(starts,SECTORS):
        require(rows,first,"B",sector+" - ")
        for off,label in ((2,"Total des passifs"),(4,"Différence de champ"),
                          (8,"Passage à la dette consolidée"),
                          (13,"Passage à la valeur nominale"),(18,"dette au sens de Maastricht")):
            require(rows,first+off,"B",label)
    records=[]
    for year,col in years:
        for first,sector in zip(starts,SECTORS):
            vals=tuple(cell(rows,first+o,col,signed=o in (13,14,15,16)) for o in BRIDGE_OFFSETS)
            tp,scope,payable,guarantee,consolidation,dep,sec,loans,nominal,acc_dep,bond,acc_loan,total=vals
            equal(f"scope components {year} {sector}",scope,payable+guarantee)
            equal(f"consolidation components {year} {sector}",consolidation,dep+sec+loans)
            gap=(nominal-acc_dep-bond-acc_loan).quantize(Decimal(".1"))
            if not gap: gap=Decimal(0)
            if abs(gap)>Decimal("3.05"):
                raise ValueError(f"Unexplained 3.104 valuation gap too large {year} {sector}")
            equal(f"Maastricht bridge {year} {sector}",total,tp-scope-consolidation-nominal)
            records.append((year,sector,*vals,gap))
    if next(r for r in records if r[:2]==(2025,"S13"))[-2].quantize(Decimal(".1"))!=Decimal("3460.1"):
        raise ValueError("3.104 audited 2025 anchor changed")
    # 3.104 S1314 2025=293.1 vs 3.102 S1314=292.6: preserve and flag.
    return BRIDGE_FIELDS,records


def extract_3105(blob):
    rows=parse_grid(blob)
    require(rows,1,"A","3.105 Passage du déficit")
    require(rows,5,"B","Déficit des administrations publiques")
    require(rows,28,"B","Variation de la dette au sens de Maastricht")
    years=year_cols(rows,3,2009,2025)
    records=[]
    for year,col in years:
        vals=tuple(cell(rows,r,col,signed=r not in (5,28)) for r in FLOW_ROWS)
        (deficit,assets,dep,sec,loan,equity,deriv,insurance,other_liab,accrued,other,
         volume,reclass,fx,buyback,accounts,gap,variation)=vals
        equal(f"acquisition components {year}",assets,dep+sec+loan+equity+deriv+insurance)
        equal(f"liability components {year}",other_liab,accrued+other)
        equal(f"volume components {year}",volume,reclass+fx+buyback)
        equal(f"stock-flow bridge {year}",variation,
              deficit+assets+other_liab+volume+accounts+gap,Decimal("0.45"))
        records.append((year,*vals))
    if records[-1][-1].quantize(Decimal(".1"))!=Decimal("154.0"):
        raise ValueError("3.105 audited 2025 anchor changed")
    return FLOW_FIELDS,records


EXTRACTORS={"3103":extract_3103,"3104":extract_3104,"3105":extract_3105}


def format_csv(fields,records):
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\n")
    writer.writerow(fields)
    for record in records:
        writer.writerow([format(value,".4f" if field=="net_debt_pct_gdp" else ".1f")
                         if isinstance(value,Decimal) else value
                         for field,value in zip(fields,record)])
    return stream.getvalue()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table",choices=("3103","3104","3105","all"),default="all")
    parser.add_argument("--xlsx-dir",type=Path)
    parser.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parents[1]/"data")
    args=parser.parse_args()
    for table in TABLES if args.table=="all" else (args.table,):
        pinned,name=TABLES[table]
        src=(args.xlsx_dir/f"t_{table}_fr.xlsx").read_bytes() if args.xlsx_dir else urllib.request.urlopen(
            f"https://www.insee.fr/fr/statistiques/fichier/8988843/t_{table}_fr.xlsx",timeout=35).read()
        digest=hashlib.sha256(src).hexdigest()
        if digest!=pinned:
            raise SystemExit(f"Insee 3.{table[1:]} SHA-256 changed: {digest}; audit first")
        fields,records=EXTRACTORS[table](src)
        args.output_dir.mkdir(parents=True,exist_ok=True)
        target=args.output_dir/name
        target.write_text(format_csv(fields,records),encoding="utf-8",newline="")
        print(f"Insee 3.{table[1:]} SHA={digest}; rows={len(records)}; path={target}")


if __name__=="__main__":
    main()
