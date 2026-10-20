"""Audit an Excel workbook used in the Nassau Candy project."""
import argparse
from pathlib import Path
import sys
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Audit an Excel workbook.")
    parser.add_argument("workbook", help="Path to an authorized .xlsx or .xlsm workbook")
    parser.add_argument("--sheet", help="Worksheet to audit; defaults to the first worksheet")
    parser.add_argument("--list-sheets", action="store_true", help="List worksheets and exit")
    args = parser.parse_args()
    path = Path(args.workbook).expanduser()
    if not path.exists():
        print(f"ERROR: Workbook not found: {path}", file=sys.stderr)
        return 2
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        print("ERROR: Provide an .xlsx or .xlsm workbook.", file=sys.stderr)
        return 2
    try:
        book = pd.ExcelFile(path)
    except Exception as exc:
        print(f"ERROR opening workbook: {exc}", file=sys.stderr)
        return 2
    print(f"Workbook: {path.resolve()}\nWorksheets:")
    for name in book.sheet_names:
        print(f" - {name}")
    if args.list_sheets:
        return 0
    sheet = args.sheet or book.sheet_names[0]
    if sheet not in book.sheet_names:
        print(f"ERROR: Worksheet '{sheet}' not found.", file=sys.stderr)
        return 2
    try:
        df = pd.read_excel(path, sheet_name=sheet)
    except Exception as exc:
        print(f"ERROR reading worksheet: {exc}", file=sys.stderr)
        return 2
    print(f"\nAudit: {sheet}")
    print(f"Rows: {len(df):,}\nColumns: {len(df.columns):,}")
    print(f"Exact duplicate rows: {int(df.duplicated().sum()):,}")
    print("\nColumn names:")
    for col in df.columns:
        print(f" - {col}")
    missing = df.isna().sum()
    missing = missing[missing > 0]
    print("\nMissing values:")
    if missing.empty:
        print("None detected.")
    else:
        print(missing.sort_values(ascending=False).to_string())
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print("\nNumeric summary:")
        print(numeric.describe().round(3).to_string())
    print("\nAudit complete. Validate column definitions and business logic before decisions.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
