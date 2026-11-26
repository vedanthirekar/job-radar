"""Build data/sponsors.csv from the Department of Labor's public H-1B (LCA) filings.

Every H-1B starts with a Labor Condition Application (LCA). DOL publishes all of them
each quarter: employer, job title, job code (SOC), worksite, status.
We count certified H-1B filings for software, data and AI job codes per employer.

Also writes data/sponsor_candidates.txt: small and mid-size tech sponsors that
are not H-1B dependent (filters out most staffing body shops). detect.py then
checks whether they use Greenhouse, Lever or Ashby.

dol.gov blocks automated downloads, so download the .xlsx files yourself
from the DOL OFLC performance data page, put them in data/dol/, and run:
    pip install python-calamine && python sponsors.py && python detect.py
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

from names import norm

ROOT = Path(__file__).parent
OUT = ROOT / "data" / "sponsors.csv"
CANDS = ROOT / "data" / "sponsor_candidates.txt"
LOCAL = ROOT / "data" / "dol"
FISCAL_YEARS = [2026, 2025]
TECH_SOC = re.compile(r"^(15-1\d{3}|15-2041|15-2051|15-2031)")
BODY_SHOP = re.compile(r"\b(staffing|consultancy|consulting|consultants|infotech|it services|"
                       r"manpower|recruit|placement|outsourc)\b", re.I)


def col(header: list[str], *names: str) -> int | None:
    h = [str(x or "").strip().upper() for x in header]
    for n in names:
        if n in h:
            return h.index(n)
    return None


def download(name: str) -> bytes | None:
    local = LOCAL / name
    if local.exists():
        print(f"  using {name}")
        return local.read_bytes()
    return None


def rows_of(xlsx: bytes):
    try:
        from python_calamine import CalamineWorkbook
        wb = CalamineWorkbook.from_filelike(io.BytesIO(xlsx))
        sheet = wb.get_sheet_by_index(0)
        yield from sheet.iter_rows()
        return
    except ImportError:
        pass
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    for r in wb.worksheets[0].iter_rows(values_only=True):
        yield list(r)


def main() -> int:
    tech = defaultdict(int)
    display = {}
    dependent = defaultdict(bool)
    first_fy = {}
    seen_cases = set()
    perm = defaultdict(int)
    got_any = False

    for fy in FISCAL_YEARS:
        for q in (4, 3, 2, 1):
            data = download(f"LCA_Disclosure_Data_FY{fy}_Q{q}.xlsx")
            if not data:
                continue
            got_any = True
            it = rows_of(data)
            header = next(it)
            c_case = col(header, "CASE_NUMBER")
            c_status = col(header, "CASE_STATUS")
            c_visa = col(header, "VISA_CLASS")
            c_soc = col(header, "SOC_CODE")
            c_emp = col(header, "EMPLOYER_NAME")
            c_dba = col(header, "TRADE_NAME_DBA")
            c_dep = col(header, "H_1B_DEPENDENT", "H1B_DEPENDENT")
            c_wil = col(header, "WILLFUL_VIOLATOR")
            if c_emp is None or c_soc is None:
                print(f"  unexpected columns in FY{fy} Q{q}, skipping")
                continue
            n = 0
            for r in it:
                case = r[c_case] if c_case is not None else None
                if case and case in seen_cases:
                    continue
                if case:
                    seen_cases.add(case)
                status = str(r[c_status] or "").lower() if c_status is not None else "certified"
                if not status.startswith("certified"):
                    continue
                if c_visa is not None and str(r[c_visa] or "").strip().upper() != "H-1B":
                    continue
                if not TECH_SOC.match(str(r[c_soc] or "")):
                    continue
                emp = str(r[c_emp] or "").strip()
                key = norm(emp)
                if not key:
                    continue
                tech[key] += 1
                display.setdefault(key, emp)
                first_fy[key] = min(first_fy.get(key, fy), fy)
                if c_dep is not None and str(r[c_dep] or "").strip().upper() in ("Y", "YES"):
                    dependent[key] = True
                if c_wil is not None and str(r[c_wil] or "").strip().upper() in ("Y", "YES"):
                    dependent[key] = True
                if c_dba is not None and r[c_dba]:
                    dk = norm(str(r[c_dba]))
                    if dk and dk != key:
                        tech[dk] += 1
                        display.setdefault(dk, str(r[c_dba]).strip())
                        first_fy[dk] = min(first_fy.get(dk, fy), fy)
                        dependent[dk] = dependent[dk] or dependent[key]
                n += 1
            print(f"  FY{fy} Q{q}: {n} tech H-1B filings")

        # Green card (PERM) filings: a strong sign of long-term sponsorship. Best effort.
        for name in (f"PERM_Disclosure_Data_New_Form_FY{fy}_Q4.xlsx", f"PERM_Disclosure_Data_FY{fy}_Q4.xlsx"):
            data = download(name)
            if not data:
                continue
            it = rows_of(data)
            header = next(it)
            c_emp = col(header, "EMP_BUSINESS_NAME", "EMPLOYER_NAME")
            c_status = col(header, "CASE_STATUS")
            if c_emp is None:
                continue
            for r in it:
                if c_status is not None and not str(r[c_status] or "").lower().startswith("certified"):
                    continue
                k = norm(str(r[c_emp] or ""))
                if k:
                    perm[k] += 1

    if not got_any:
        print("No DOL files found in data/dol/. Download them from the DOL OFLC performance data page first.")
        return 1

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["employer_norm", "employer_name", "tech_lcas", "perm", "h1b_dependent", "since_fy"])
        for k in sorted(tech, key=lambda k: -tech[k]):
            w.writerow([k, display[k], tech[k], perm.get(k, 0), "Y" if dependent[k] else "",
                        first_fy.get(k, FISCAL_YEARS[-1])])

    # Candidates for the watch list: real product companies, roughly small to mid size.
    def nice(n: str) -> str:
        return n.title() if n.isupper() else n

    cands = [nice(display[k]) for k in tech
             if 1 <= tech[k] <= 80 and not dependent[k] and not BODY_SHOP.search(display[k])]
    cands.sort(key=lambda name: -tech[norm(name)])
    CANDS.write_text("\n".join(cands[:5000]) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(tech)} sponsoring employers; {min(len(cands), 5000)} watch-list candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
