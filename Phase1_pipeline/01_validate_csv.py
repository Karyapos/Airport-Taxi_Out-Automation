import pandas as pd
import sys

EXPECTED_COLUMNS = [
    "timestamp",
    "carrier",
    "distance_scheduled",
    "departures_traffic",
    "arrivals_traffic",
    "wind_speed",
    "wind_direction",
    "taxi_out",
]

INT_COLUMNS    = {"taxi_out", "departures_traffic", "arrivals_traffic", "distance_scheduled", "wind_speed"}
STR_COLUMNS    = {"carrier", "wind_direction"}
DATE_COLUMNS   = {"timestamp"}
POSITIVE_CHECK = INT_COLUMNS  # all must be > 0


def validate(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # ── 1. column order / names ──────────────────────────────────────────────
    if list(df.columns) != EXPECTED_COLUMNS:
        print(f"ERROR: wrong columns or order.\n  got:      {list(df.columns)}\n  expected: {EXPECTED_COLUMNS}")
        sys.exit(1)

    # ── 2. drop missing rows ─────────────────────────────────────────────────
    original_len = len(df)
    df.dropna(inplace=True)
    dropped = original_len - len(df)

    if dropped / original_len > 0.20:
        print(f"ERROR: {dropped}/{original_len} rows dropped ({dropped/original_len:.1%}) — too many missing values.")
        sys.exit(1)

    if dropped:
        print(f"INFO: {dropped} row(s) with missing values removed.")

    # ── 3. type checks ───────────────────────────────────────────────────────
    for col in INT_COLUMNS:
        if not pd.api.types.is_integer_dtype(df[col]):
            # try coercing
            coerced = pd.to_numeric(df[col], errors="coerce")
            if coerced.isna().any() or not (coerced % 1 == 0).all():
                print(f"ERROR: '{col}' must be integer — got wrong type/values.")
                sys.exit(1)
            df[col] = coerced.astype(int)

    for col in STR_COLUMNS:
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"ERROR: '{col}' must be string — got numeric.")
            sys.exit(1)

    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        if df[col].isna().any():
            print(f"ERROR: '{col}' contains values that are not valid timestamps.")
            sys.exit(1)

    # ── 4. all numeric columns > 0 ───────────────────────────────────────────
    for col in POSITIVE_CHECK:
        if (df[col] < 0).any():
            print(f"ERROR: '{col}' must be >= 0 — found zero or negative values.")
            sys.exit(1)

    print("OK: all checks passed.")
    return df

if len(sys.argv)!= 2:
    print ( "Usage: python validate_csv.py <path_to_csv>")
    sys.exit(1)
validate(sys.argv[1])